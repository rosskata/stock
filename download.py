"""MAin module to download data for analysis"""

import yfinance as yf
import nasdaq_lib as ndl


tickers = ndl.NasdaqTickerSymbol().download_ticker_symbols()


FOLDER_PATH = "./stock_data"
START_DATE = "2022-05-19"
END_DATE = "2022-05-20"


for ticker in tickers:
    stock_data = yf.download(ticker, start=START_DATE, end=END_DATE)
    file_name = f"{ticker}_{START_DATE}_{END_DATE}.csv"
    file_path = f"{FOLDER_PATH}/{file_name}"
    print ("file path is : ", file_path)
    print('Getting data for ', ticker)
    print('This is where the downloader should start downloading...')
    downloader = ndl.StockDataDownloader(FOLDER_PATH, START_DATE, END_DATE, ticker)
    downloader.download_data()
