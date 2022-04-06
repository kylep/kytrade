# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kytrade',
 'kytrade.api',
 'kytrade.api.client',
 'kytrade.api.server',
 'kytrade.cli',
 'kytrade.cli.ps',
 'kytrade.cli.strat',
 'kytrade.data',
 'kytrade.ps',
 'kytrade.strategy']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0',
 'SQLAlchemy>=1.4.34,<2.0.0',
 'alpha-vantage>=2.3.1,<3.0.0',
 'beautifultable>=1.0.1,<2.0.0',
 'click>=8.1.2,<9.0.0',
 'gmpy2>=2.1.2,<3.0.0',
 'ib-insync>=0.9.70,<0.10.0',
 'matplotlib>=3.5.1,<4.0.0',
 'mysqlclient>=2.1.0,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'torch>=1.11.0,<2.0.0',
 'yfinance>=0.1.70,<0.2.0']

entry_points = \
{'console_scripts': ['kt = kytrade.cli.main:shell']}

setup_kwargs = {
    'name': 'kytrade',
    'version': '1.0.0',
    'description': "Kyle's trading tool",
    'long_description': None,
    'author': 'kylep',
    'author_email': 'kyle@pericak.com',
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
