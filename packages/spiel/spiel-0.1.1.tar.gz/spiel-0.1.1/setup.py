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
    'version': '0.1.1',
    'description': 'A framework for building and presenting richly-styled presentations in your terminal using Python.',
    'long_description': '# Spiel\n\n![PyPI](https://img.shields.io/pypi/v/spiel)\n[![Documentation Status](https://readthedocs.org/projects/spiel/badge/?version=latest)](https://spiel.readthedocs.io/en/latest/?badge=latest)\n![PyPI - License](https://img.shields.io/pypi/l/spiel)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/spiel/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/spiel/main)\n[![codecov](https://codecov.io/gh/JoshKarpel/spiel/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/spiel)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/spiel)\n![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/spiel)\n\nSpiel is a framework for building and presenting richly-styled presentations in your terminal using Python.\n\nTo see what Spiel can do, install it (`pip install spiel`), then run this command to view the demonstration deck:\n```bash\n$ spiel demo present\n```\n',
    'author': 'JoshKarpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoshKarpel/spiel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
