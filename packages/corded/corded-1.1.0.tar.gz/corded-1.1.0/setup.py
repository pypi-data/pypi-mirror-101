# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corded', 'corded.caching', 'corded.http', 'corded.objects', 'corded.ws']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'corded',
    'version': '1.1.0',
    'description': 'A lightweight, extensible client library for Discord bots',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
