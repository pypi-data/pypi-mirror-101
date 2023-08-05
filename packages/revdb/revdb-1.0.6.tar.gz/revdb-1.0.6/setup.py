# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['revdb']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=2.1.0,<3.0.0',
 'mongoengine>=0.23.0,<0.24.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'revdb',
    'version': '1.0.6',
    'description': '',
    'long_description': None,
    'author': 'Chien',
    'author_email': 'a0186163@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
