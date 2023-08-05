# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokesummary', 'pokesummary.data']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pokesummary = pokesummary.__main__:main']}

setup_kwargs = {
    'name': 'pokesummary',
    'version': '0.2.0',
    'description': 'An easy-to-use, informative command line interface (CLI) for accessing Pokémon summaries.',
    'long_description': "# Pokésummary\nAn easy-to-use, informative command line interface (CLI)\nfor accessing Pokémon summaries.\n\nCurrently in development.\n\n## Screenshot\n![image](https://user-images.githubusercontent.com/29507110/113600322-d52a6a00-960d-11eb-8813-ed86f394adf2.png)\n\n## Usage\n```\nusage: pokesummary [-h] [-i] [pokemon [pokemon ...]]\n\nGet summaries for a Pokémon or multiple Pokémon.\n\npositional arguments:\n  pokemon            the Pokémon to look up\n\noptional arguments:\n  -h, --help         show this help message and exit\n  -i, --interactive  run interactively\n```\n\n## Installation\n\n### Requirements\n- Python 3.7+\n- A terminal supporting ANSI escape codes\n(most Linux and macOS terminals,\nsee [here](https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling) for Windows)\n\n### Manual Install\n1. Clone or download the repository\n2. Install using pip or Poetry\n\nUsing pip:\n```sh\npip3 install .\n```\n\nUsing poetry:\n```sh\npoetry install\n```\n\n## Acknowledgements\n- Type chart from [Pokémon Database](https://pokemondb.net/type)\n- Pokémon data from [Yu-Chi Chiang's fixed database](https://www.kaggle.com/mrdew25/pokemon-database/discussion/165031)\n",
    'author': 'Fisher Sun',
    'author_email': 'fisher521.fs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tactlessfish/pokesummary',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
