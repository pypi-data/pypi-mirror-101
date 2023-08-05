import re
import time
import requests
import json
import logging
import concurrent.futures
import pandas as pd
import pandas_datareader as pdr


log_format = '%(levelname)s: %(module)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def get_ticker(ticker: str, start_date: str, end_date: str):
    """
    ticker: string, e.g. 'AAPL'
    start_date: string '2020-01-01'
    end_date: string, e.g. '2020-01-31'
    """
    try:
        df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
        df['Ticker'] = ticker
        return df
    except Exception as e:
        logging.warning(f"{e}: {ticker}")

def download_market(market: str, start_date: str, end_date: str):
    """
    market: string e.g. 'Nasdaq'
    start_date: string '2020-01-01'
    end_date: string, e.g. '2020-01-31'
    """

    if market == 'Nasdaq':
        tickers = set(pd.read_csv('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt',
                              error_bad_lines=False, sep='|').Symbol.tolist())

    logging.info("Found %d tickers on nasdaqtrader.com"%len(tickers))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(get_prices, ticker, start_date, end_date) for ticker in tickers}
        def gen():
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                    if isinstance(data, pd.DataFrame):
                        yield data
                except Exception as exc:
                    logging.warning(exc)

        df = pd.concat(gen())
    df.columns = list(map(lambda x: x.capitalize(), df.columns))
    df = df.rename(columns={'Adjclose': 'AdjClose'})
    df = df[['Ticker', 'Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'AdjClose']]

    return df

def get_prices(ticker: str, start_date: str, end_date: str):

    start = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
    end = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))
    url = f"https://finance.yahoo.com/quote/{ticker}/history?period1={start}&period2={end}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    resp = requests.get(url)
    ptrn = r"root\.App\.main = (.*?);\n}\(this\)\);"
    j = json.loads(re.search(ptrn, resp.text, re.DOTALL).group(1))
    data = j["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]["prices"]
    # remove corp actions
    data = list(filter(lambda x: 'type' not in x.keys(), data))
    df = pd.DataFrame(data)
    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'], unit='s').dt.date
        df['Ticker'] = ticker
        return df
    logging.warning(f"No data downloaded for {ticker}")

