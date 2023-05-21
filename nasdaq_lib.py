"""Library to enable downloading of all nasdaq tickers that are traded currently"""
import pandas as pd
import yfinance as yf


class NasdaqTickerSymbol:
    """
    Grabs the file that contains the latest data about all traded symbols on
    the NASDAQ. The data comes from a text file that is then processed to
    collect only the tickers
    """

    def __init__(self):
        pass

    def download_ticker_symbols(self):
        """
        download the ticker symbols. USes data available from nasdaq to
        download all traded ticker symbols
        """
        url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt'
        data_file = pd.read_csv(url, delimiter='|')
        data_file = data_file[data_file['Test Issue']
                              == 'N']  # remove test issues
        # remove non-active issues
        data_file = data_file[data_file['Financial Status'] == 'N']
        data_file = data_file[data_file['ETF'] == 'N']  # remove ETFs
        data_file = data_file[['Symbol']]
        data_file = data_file.rename(columns={'Symbol': 'Ticker'})

        return data_file['Ticker'].tolist()

    def __str__(self):
        return f"{NasdaqTickerSymbol} object"

    def __repr__(self):
        return f"{NasdaqTickerSymbol()}"


class StockDataDownloader:
    """
    Used to download the ticker data. USes provided ticker symbol and
    downloads historical data
    from Yahoo finance for the selected ticker between the START and END dates
    """

    def __init__(self, folder_path, start_date, end_date, ticker_symbol):
        self.folder_path = folder_path
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_symbol = ticker_symbol
        self.file_name = f"{self.ticker_symbol}_{self.start_date}_{self.end_date}.csv"
        self.file_path = f"{self.folder_path}/{self.file_name}"

    def download_data(self):
        """The downloader method"""
        stock_data = yf.download(
            self.ticker_symbol, start=self.start_date, end=self.end_date)

        stock_data.to_csv(self.file_path)
        print(
            f"Stock data for {self.ticker_symbol} saved to {self.file_path}.")

        # Read in the CSV file and convert the 'Date' column to a datetime format
        stock_data = pd.read_csv(self.file_path, parse_dates=['Date'])

        # Calculate moving averages
        stock_data['SMA20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()

        print("SMA20: ", stock_data['SMA20'])
        print("SMA50: ", stock_data['SMA50'])
        print("SMA200: ", stock_data['SMA200'])

    def __str__(self):
        return f"StockDataDownloader instance:\n" \
               f"Folder Path: {self.folder_path}\n" \
               f"Start Date: {self.start_date}\n" \
               f"End Date: {self.end_date}\n" \
               f"Ticker Symbol: {self.ticker_symbol}"

    def __repr__(self):
        path = self.folder_path
        start_date = self.start_date
        end_date = self.end_date
        ticker = self.ticker_symbol
        return f"StockDataDownloader({path}, {start_date}, {end_date}, {ticker})"
