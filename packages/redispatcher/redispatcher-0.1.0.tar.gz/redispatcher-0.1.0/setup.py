# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redispatcher']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'isort>=5.8.0,<6.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'redispatcher',
    'version': '0.1.0',
    'description': 'Toolset for asynchronous message processing backed by Redis as the message broker',
    'long_description': None,
    'author': 'Rafal Stapinski',
    'author_email': 'stapinskirafal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
