# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flamingo']

package_data = \
{'': ['*']}

install_requires = \
['click', 'requests', 'tabulate']

entry_points = \
{'console_scripts': ['flamingo = flamingo.main:cli']}

setup_kwargs = {
    'name': 'flamingo-cli',
    'version': '1.3.1',
    'description': 'Flamingo Command Line Interface',
    'long_description': None,
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
