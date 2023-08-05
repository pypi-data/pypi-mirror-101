# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['multicommand']
setup_kwargs = {
    'name': 'multicommand',
    'version': '0.0.6',
    'description': 'Simple subcommand CLIs with argparse',
    'long_description': "# multicommand\n\nSimple subcommand CLIs with argparse.\n\n[![PyPI Version](https://img.shields.io/pypi/v/multicommand.svg)](https://pypi.org/project/multicommand/)\n\n## Installation\n\n```bash\npip install multicommand\n```\n\n## Overview\n\n`multicommand` enables you to **easily** write CLIs with deeply nested commands using vanilla argparse.\n\nJust create a directory structure that reflects the command structure you want, add a parser to each module (don't worry about hooking them up!), and multicommand will do the rest.\n\nmulticommand turns a directory structure like this:\n\n```text\ncommands/unary/negate.py\ncommands/binary/add.py\ncommands/binary/divide.py\ncommands/binary/multiply.py\ncommands/binary/subtract.py\n```\n\nInto a command line application like this:\n\n```bash\nmycli unary negate ...\nmycli binary add ...\nmycli binary divide ...\nmycli binary multiply ...\nmycli binary subtract ...\n```\n\nAll multicommand needs is for each module to define a module-level `parser` variable which points to an instance of `argparse.ArgumentParser`.\n\n## Getting Started\n\nSee the [simple example](https://github.com/andrewrosss/multicommand/tree/master/examples/01_simple).\n",
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/multicommand',
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
