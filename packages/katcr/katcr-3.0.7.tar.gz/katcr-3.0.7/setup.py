# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katcr', 'katcr.engines']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.2,<4.0.0',
 'cleo',
 'cutie>=0.2.2,<0.3.0',
 'feedparser>=6.0.2,<7.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'torrentmirror',
 'xdg>=5.0.1,<6.0.0']

extras_require = \
{':extra == "bot"': ['aiogram>=2.11.2,<3.0.0']}

entry_points = \
{'console_scripts': ['bot = katcr:bot', 'katcr = katcr:main']}

setup_kwargs = {
    'name': 'katcr',
    'version': '3.0.7',
    'description': 'KickassTorrents CLI and Telegram bot',
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
