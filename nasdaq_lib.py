import pandas as pd
import yfinance as yf

class NasdaqTickerSymbol:
    def __init__(self):
        pass

    def download_ticker_symbols(self):
        url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt'
        df = pd.read_csv(url, delimiter='|')
        df = df[df['Test Issue'] == 'N']  # remove test issues
        df = df[df['Financial Status'] == 'N']  # remove non-active issues
        df = df[df['ETF'] == 'N']  # remove ETFs
        df = df[['Symbol']]
        df = df.rename(columns={'Symbol': 'Ticker'})

        return df['Ticker'].tolist()

    def __str__(self):
        return f"NasdaqTickerSymbol object"

    def __repr__(self):
        return f"NasdaqTickerSymbol()"



class StockDataDownloader:
    def __init__(self, folder_path, start_date, end_date, ticker_symbol):
        self.folder_path = folder_path
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_symbol = ticker_symbol
        self.file_name = f"{self.ticker_symbol}_{self.start_date}_{self.end_date}.csv"        
        self.file_path = f"{self.folder_path}/{self.file_name}"
    
    def download_data(self):
        stock_data = yf.download(self.ticker_symbol, start=self.start_date, end=self.end_date)

        stock_data.to_csv(self.file_path)
        print(f"Stock data for {self.ticker_symbol} saved to {self.file_path}.")
    
        # Read in the CSV file and convert the 'Date' column to a datetime format
        stock_data = pd.read_csv(self.file_path, parse_dates=['Date'])
        
        # Calculate moving averages
        stock_data['SMA20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()

        print ("SMA20: ", stock_data['SMA20'])
        print ("SMA50: ", stock_data['SMA50'])
        print ("SMA200: ", stock_data['SMA200'])
        
        
    def __str__(self):
        return f"StockDataDownloader instance:\n" \
               f"Folder Path: {self.folder_path}\n" \
               f"Start Date: {self.start_date}\n" \
               f"End Date: {self.end_date}\n" \
               f"Ticker Symbol: {self.ticker_symbol}"

    
    def __repr__(self):
        return f"StockDataDownloader({self.folder_path}, {self.start_date}, {self.end_date}, {self.ticker_symbol})"