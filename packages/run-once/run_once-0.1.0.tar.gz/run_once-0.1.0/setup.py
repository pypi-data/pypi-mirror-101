# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['run_once']
install_requires = \
['grpcio-tools>=1.15,<2.0', 'grpcio>=1.15,<2.0', 'joblib>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'run-once',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daeyun Shin',
    'author_email': 'daeyuns@uci.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
