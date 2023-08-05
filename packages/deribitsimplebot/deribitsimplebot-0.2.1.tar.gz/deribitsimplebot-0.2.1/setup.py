# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deribitsimplebot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'anyio>=2.1.0,<3.0.0',
 'json5>=0.9.5,<0.10.0',
 'mysql-connector-python>=8.0.23,<9.0.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'deribitsimplebot',
    'version': '0.2.1',
    'description': 'Class set for the implementation of a simple bot working with the Deribit crypto exchange',
    'long_description': None,
    'author': 'Eliseev Nikolay',
    'author_email': 'n.a.eliseev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/n-eliseev/deribitsimplebot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
