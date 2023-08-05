# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkace_cli', 'linkace_cli.api', 'linkace_cli.cli', 'linkace_cli.models']

package_data = \
{'': ['*'], 'linkace_cli.cli': ['templates/*']}

install_requires = \
['marshmallow>=3.10.0,<4.0.0',
 'pylint>=2.6.0,<3.0.0',
 'requests>=2.25.0,<3.0.0',
 'rich>=9.5.1,<10.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['linkace = linkace_cli:main']}

setup_kwargs = {
    'name': 'linkace-cli',
    'version': '1.1.0',
    'description': 'A CLI for the LinkAce API',
    'long_description': '# linkace-cli\nA CLI for the API of LinkAce (https://github.com/Kovah/LinkAce)\n\n[![asciicast](https://asciinema.org/a/UO74II9ajDXaNjbwpmxaFdWZX.svg)](https://asciinema.org/a/UO74II9ajDXaNjbwpmxaFdWZX)\n\n![PyPi version](https://pypip.in/v/linkace-cli/badge.png)\n![TheJokersThief](https://circleci.com/gh/TheJokersThief/linkace-cli.svg?style=svg)\n\n- [linkace-cli](#linkace-cli)\n- [Install](#install)\n- [Usage](#usage)\n  - [Links](#links)\n  - [Lists](#lists)\n  - [Tags](#tags)\n  - [Search](#search)\n\n# Install\n\n```\npip install linkace-cli\n```\n\n# Usage\n## Links\n\n```\n$ linkace link --help\nUsage: linkace link [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create  Create a new link with the info provided.\n  delete  Delete a link with the given ID\n  get     Get all links or, if --id is provided, get the details of just\n          one...\n\n  update  Update a link with the info provided.\n```\n\n## Lists\n\n```\n$ linkace list --help\nUsage: linkace list [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create  Create a new link with the info provided.\n  delete  Delete a link with the given ID\n  get     Get all lists or, if --id is provided, get the details of just\n          one...\n\n  update  Update a list with the info provided.\n```\n\n## Tags\n\n```\n$ linkace tag --help\nUsage: linkace tag [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create  Create a new tag with the info provided.\n  delete  Delete a tag with the given ID\n  get     Get all tags or, if --id is provided, get the details of just one...\n  update  Update a tag with the info provided.\n```\n\n## Search\n\n```\n$ linkace search --help\nUsage: linkace search [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  by-list   Search for links in lists\n  by-query  Search for tags by query\n  by-tag    Search for links with tags\n```\n',
    'author': 'Evan Smith',
    'author_email': 'me@iamevan.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
