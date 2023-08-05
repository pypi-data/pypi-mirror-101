# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yahoo_prices']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.23,<2.0.0',
 'pandas-datareader>=0.9.0,<0.10.0',
 'pandas>=1.2.3,<2.0.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'yahoo-prices',
    'version': '0.3.7',
    'description': 'Light weight python package for downloading yahoo-finance prices',
    'long_description': 'This python package downloads Yahoo Finance stock prices and \nwrites it to a local sqlalchemy database file\n\n# Installation:\n\npip install yahoo-prices\n\n# Examples\n\n>>> from yahoo_prices import update_db\n>>> from yahoo_prices.prices_table import create_table\n>>> from sqlalchemy.orm import sessionmaker\n>>> engine = create_table()\n>>> Session = sessionmaker(bind=engine)\n>>> session = Session()\n>>> apple_df = get_ticker("AAPL", "2021-01-01", "2021-12-31")\n>>> apple_df = apple_df.reset_index()\n>>> apple_df = update_db.prepare_data(apple_df, engine)\n>>> update_db(apple_df, session)\n',
    'author': 'aghazaly',
    'author_email': 'ahmed.ghazaly.1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
