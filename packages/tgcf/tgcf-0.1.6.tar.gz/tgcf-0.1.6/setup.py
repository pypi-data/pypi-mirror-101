# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgcf', 'tgcf.extensions']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Telethon>=1.20,<2.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptg>=0.2.post2,<0.3',
 'hachoir>=3.1.2,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tgcf = tgcf:cli.app']}

setup_kwargs = {
    'name': 'tgcf',
    'version': '0.1.6',
    'description': 'Coming soon...',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
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
