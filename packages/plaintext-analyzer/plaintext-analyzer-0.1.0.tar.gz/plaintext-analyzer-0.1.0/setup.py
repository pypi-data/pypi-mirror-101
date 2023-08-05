# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plaintext_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'sencore>=0.1.7,<0.2.0', 'x2cdict>=0.1.40,<0.2.0']

entry_points = \
{'console_scripts': ['pta_phrase = plaintext_analyzer.entry:parser_phrase',
                     'pta_vocab = plaintext_analyzer.entry:parser_vocab']}

setup_kwargs = {
    'name': 'plaintext-analyzer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
