# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydid', 'pydid.doc']

package_data = \
{'': ['*']}

install_requires = \
['voluptuous>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'pydid',
    'version': '0.2.3',
    'description': 'Python library for validating, constructing, and representing DIDs and DID Documents',
    'long_description': '# PyDID\n\n[![pypi release](https://img.shields.io/pypi/v/pydid)](https://pypi.org/project/pydid/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nPython library for validating, constructing, and representing DIDs and DID Documents.\n\n## Installation\n\nUsing a virtual environment is generally recommended:\n\n```sh\n$ python -m venv env\n$ source env/bin/activate\n```\n\nInstall with pip:\n\n```sh\n$ pip install pydid\n```\n\n## Development\n\nThis project is managed with [Poetry](https://python-poetry.org/).\n\nTo begin making code changes, clone this repo and do the following to install\ndependencies:\n\n```sh\n$ python -m venv env\n$ source env/bin/activate\n$ pip install poetry\n$ poetry install\n```\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md).\n',
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbluhm/pydid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
