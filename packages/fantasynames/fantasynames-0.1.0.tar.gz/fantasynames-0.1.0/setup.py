# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fantasynames']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0', 'flake8>=3.9.0,<4.0.0', 'mypy>=0.812,<0.813']

setup_kwargs = {
    'name': 'fantasynames',
    'version': '0.1.0',
    'description': 'A fantasy themed random name generator.',
    'long_description': None,
    'author': 'Jessica Peck',
    'author_email': 'jessypeck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jessypeck/fantasynames',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
