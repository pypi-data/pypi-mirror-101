import contextlib
import copy
import functools
import configparser
import os
import random
import socket
import sys
import time
import typing
from os import path

import grpc
from google.protobuf import duration_pb2
from grpc._channel import _InactiveRpcError

rpc_timeout = 10


@contextlib.contextmanager
def add_sys_path(p):
    if p not in sys.path:
        sys.path.insert(0, p)
    try:
        yield
    finally:
        if p in sys.path:
            sys.path.remove(p)


with add_sys_path(path.abspath(path.join(__file__, "../generated/proto"))):
    from generated.proto import distlock_pb2
    from generated.proto import distlock_pb2_grpc


@functools.lru_cache(1)
def worker_name():
    return "{}_{:05d}_{:05d}".format(
        socket.gethostname(),
        os.getpid(),
        os.getppid(),
    )


def _with_retry(fn, max_retry_count=20, sleep_seconds=5):
    retry_count = 0
    while True:
        try:
            return fn()
        except _InactiveRpcError as ex:
            if retry_count > max_retry_count:
                raise TimeoutError("Max retries exceeded. {}".format(ex))
            retry_count += 1
            # lock_service_client() is expected to be called from `fn()`.
            _prepare_client.cache_clear()
            time.sleep(sleep_seconds)


def try_lock(
        lock: distlock_pb2.Lock, force=False
) -> typing.Optional[distlock_pb2.Lock]:
    client = lock_service_client()
    request = distlock_pb2.AcquireLockRequest(
        lock=lock,
        overwrite=force,
    )
    response: distlock_pb2.AcquireLockResponse = client.AcquireLock(
        request, timeout=rpc_timeout
    )
    is_successful = response.HasField("acquired_lock")
    return response.acquired_lock if is_successful else None


def force_lock_async(lock: distlock_pb2.Lock, callback=None):
    client = lock_service_client()
    request = distlock_pb2.AcquireLockRequest(
        lock=lock,
        overwrite=True,
    )
    future: grpc.Future = client.AcquireLock.future(request)

    if callback is not None:
        future.add_done_callback(callback)

    assert isinstance(future, grpc.Future)
    return future


def release_lock_async(key: str, callback=None):
    assert isinstance(key, str), key
    client = lock_service_client()
    request = distlock_pb2.ReleaseLockRequest(
        lock=make_lock(key=key),
        return_released_lock=False,
    )
    future: grpc.Future = client.ReleaseLock.future(request)

    if callback is not None:
        future.add_done_callback(callback)

    assert isinstance(future, grpc.Future)
    return future


def is_ascii(s):
    try:
        s.encode("ascii")
    except UnicodeEncodeError:
        return False
    else:
        return True


def make_lock(key, expiration_seconds=0, owner_name=None, force_ascii=True):
    # expiration_seconds=0 means no expiration.
    if force_ascii:
        assert is_ascii(key), key
    return distlock_pb2.Lock(
        global_id=key,
        expires_in=make_duration(expiration_seconds),
        last_owner_name=owner_name,
    )


def search_keys_by_prefix(key_prefix: str, is_expired=None):
    client = lock_service_client()
    end_key = key_prefix + "\U0010fffe"  # 244, 143, 191, 191
    start_key = key_prefix

    ret = []

    if is_expired is None:
        includes = None
    else:
        includes = [
            distlock_pb2.LockMatchExpression(
                global_id_regex=r".*", is_expired=is_expired
            )
        ]

    while True:
        request = distlock_pb2.ListLocksRequest(
            start_key=start_key,
            end_key=end_key,
            includes=includes,
        )
        response: distlock_pb2.ListLocksResponse = client.ListLocks(
            request, timeout=rpc_timeout
        )
        if len(response.locks) == 0:
            break
        elif len(response.locks) == 1:
            ret.append(response.locks[0].global_id)
            break
        else:
            start_key = response.locks[-1].global_id
            ret.extend([item.global_id for item in response.locks[:-1]])
    return ret


def at_most_every(_func=None, *, seconds, key):
    def decorator_unique_task(func):
        @functools.wraps(func)
        def wrapper_unique_task(*args, **kwargs):
            acquired_lock = try_lock(
                lock=distlock_pb2.Lock(
                    global_id=key,
                    expires_in=seconds,
                    last_owner_name=worker_name(),
                )
            )
            if acquired_lock is not None:
                return func(*args, **kwargs)
            else:
                return

        return wrapper_unique_task

    if _func is None:
        return decorator_unique_task
    else:
        return decorator_unique_task(_func)


def make_duration(seconds):
    return duration_pb2.Duration(
        seconds=int(seconds), nanos=int((seconds - int(seconds)) * 1e9)
    )


def lock_service_client(address: str = None, port: int = None):
    config = configparser.ConfigParser(
        defaults={"address": "127.0.0.1", "port": "22113"}
    )
    config.read(path.expanduser("~/.run_once.ini"))

    if address is None:
        address = config["DEFAULT"]["address"]

    if port is None:
        port = int(config["DEFAULT"]["port"])

    assert isinstance(address, str), address
    assert isinstance(port, int), port

    ret = _prepare_client(address=address, port=port)
    return ret


@functools.lru_cache(1)
def _prepare_client(address: str, port: int):
    hostname = f"{address}:{port}"

    channel = grpc.insecure_channel(
        hostname,
        options=(
            ("grpc.keepalive_time_ms", 10000),
            ("grpc.keepalive_timeout_ms", 5000),
            ("grpc.keepalive_permit_without_calls", True),
            ("grpc.http2.bdp_probe", True),
        ),
    )
    client = distlock_pb2_grpc.LockManagerServiceStub(channel)
    return client


class UniqueTaskIterator:
    def __init__(
            self,
            keys: typing.MutableSequence[str],
            expiration_seconds: typing.Union[int, float],
            shuffle=False,
            chunksize=10,
            random_seed=None,
    ):
        self.keys = copy.deepcopy(keys)
        self.shuffle = shuffle
        self.chunksize = chunksize
        self.expiration_seconds = expiration_seconds
        self.default_rpc_timeout = 30
        self.random_seed = random_seed
        self.random = random.Random(self.random_seed)

    def __iter__(self):
        self.i = 0
        if self.shuffle:
            random.shuffle(self.keys)
        return self

    def _acquire_next_available(self):
        # Modifies self.i
        # If no lock is acquired, it will try the next range.
        while True:
            client = lock_service_client()
            request = distlock_pb2.AcquireManyRequest(
                requests=[
                    distlock_pb2.AcquireLockRequest(
                        lock=make_lock(
                            key, expiration_seconds=self.expiration_seconds
                        )
                    )
                    for key in self.keys[self.i: self.i + self.chunksize]
                ],
                max_acquired_locks=1,
            )
            responses: distlock_pb2.AcquireManyResponse = client.AcquireMany(
                request, timeout=self.default_rpc_timeout
            ).responses
            if len(responses) == 0:
                return None
            self.i += len(responses)
            if responses[-1].HasField("acquired_lock"):
                ret = responses[-1].acquired_lock.global_id
                assert ret
                return ret

    def __next__(self):
        next_key = _with_retry(
            lambda: self._acquire_next_available(),
            max_retry_count=20,
            sleep_seconds=5,
        )
        if next_key is None:
            raise StopIteration
        return next_key

    def mark_completed(self, key):
        lock = try_lock(make_lock(key, expiration_seconds=0), force=True)
        assert lock is not None
        return lock

    def mark_failed(self, key):
        release_lock_async(key)
