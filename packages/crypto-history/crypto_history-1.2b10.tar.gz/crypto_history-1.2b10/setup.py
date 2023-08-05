# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crypto_history',
 'crypto_history.data_container',
 'crypto_history.emit_data',
 'crypto_history.stock_market',
 'crypto_history.utilities']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.5,<2.0.0',
 'python-binance-async>=0.7.4-beta.0,<0.8.0',
 'xarray>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'crypto-history',
    'version': '1.2b10',
    'description': 'crypto_history is a python package for extracting history of crypto-currencies from various exchanges and presenting them in a tabular data-format',
    'long_description': None,
    'author': 'Vikramaditya Gaonkar',
    'author_email': 'vikramaditya91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
