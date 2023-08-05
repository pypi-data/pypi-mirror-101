This python package downloads Yahoo Finance stock prices and 
writes it to a local sqlalchemy database file

# Installation:

pip install yahoo-prices

# Examples

>>> from yahoo_prices import update_db
>>> from yahoo_prices.prices_table import create_table
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_table()
>>> Session = sessionmaker(bind=engine)
>>> session = Session()
>>> apple_df = get_ticker("AAPL", "2021-01-01", "2021-12-31")
>>> apple_df = apple_df.reset_index()
>>> apple_df = update_db.prepare_data(apple_df, engine)
>>> update_db(apple_df, session)
