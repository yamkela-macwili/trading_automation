import yfinance as yf  # For stock data
import pandas as pd

def get_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start = start_date, end=end_date)
        return data
    except Exception as e:
        print(e)
        
def save_data(stock_data, file_name):
    df = pd.DataFrame(stock_data)
    df.to_csv(file_name, index=False)
        