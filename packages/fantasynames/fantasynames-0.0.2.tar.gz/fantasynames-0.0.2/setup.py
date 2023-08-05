# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fantasynames']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0']

setup_kwargs = {
    'name': 'fantasynames',
    'version': '0.0.2',
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
