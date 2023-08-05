# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spiel', 'spiel.demo']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'rich>=10.0.0,<11.0.0',
 'typer>=0.3.2,<0.4.0',
 'watchdog>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['spiel = spiel.main:app']}

setup_kwargs = {
    'name': 'spiel',
    'version': '0.1.0',
    'description': 'A framework for building and presenting richly-styled presentations in your terminal using Python.',
    'long_description': None,
    'author': 'JoshKarpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
