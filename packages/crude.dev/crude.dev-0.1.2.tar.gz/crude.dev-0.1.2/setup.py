# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crude_dev']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0',
 'msgpack>=1.0.2,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['crude = crude_dev.cli:main', 'run = crude_dev.cli:main']}

setup_kwargs = {
    'name': 'crude.dev',
    'version': '0.1.2',
    'description': 'crude.dev api client',
    'long_description': None,
    'author': 'Janto Dreijer',
    'author_email': 'jantod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://crude.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
