import data
import pandas as pd    # For data manipulation
import numpy as np     # For numerical operations
import matplotlib.pyplot as plt  # For visualizations

# Define parameters
ticker = "AAPL"  # Apple stock
start_date = "2010-01-01"
end_date = "2025-01-01"

# Fetch historical stock data
aapl_data = data.get_data(ticker, start_date, end_date)

# Display first few rows
print(aapl_data)

# Calculate Simple Moving Averages
short_window = 50  # Short-term SMA
long_window = 200  # Long-term SMA

aapl_data['SMA50'] = aapl_data['Close'].rolling(window=short_window).mean()

aapl_data['SMA200'] = aapl_data['Close'].rolling(window=long_window).mean()

# Define signals
aapl_data['Signal'] = 0  # Initialize Signal column with 0
aapl_data.loc[aapl_data['SMA50'] > aapl_data['SMA200'], 'Signal'] = 1  # Buy
aapl_data.loc[aapl_data['SMA50'] < aapl_data['SMA200'], 'Signal'] = -1  # Sell

data.save_data(aapl_data, ticker)

# Create positions (shift signals to avoid look-ahead bias)
aapl_data['Position'] = aapl_data['Signal'].shift(1)

# Calculate daily percentage change in stock prices
aapl_data['Daily Return'] = aapl_data['Close'].pct_change()

# Calculate returns based on the strategy
aapl_data['Strategy Return'] = aapl_data['Position'] * aapl_data['Daily Return']

# Calculate cumulative returns
aapl_data['Cumulative Market Return'] = (1 + aapl_data['Daily Return']).cumprod()
aapl_data['Cumulative Strategy Return'] = (1 + aapl_data['Strategy Return']).cumprod()


# plt.figure(figsize=(14, 7))
# plt.plot(aapl_data['Close'], label='Close Price', alpha=0.5)
# plt.plot(aapl_data['SMA50'], label='SMA50', alpha=0.75)
# plt.plot(aapl_data['SMA200'], label='SMA200', alpha=0.75)
# plt.title(f"{ticker} Price and Moving Averages")
# plt.legend()
# plt.show()

# plt.figure(figsize=(14, 7))
# plt.plot(aapl_data['Cumulative Market Return'], label='Market Return', alpha=0.75)
# plt.plot(aapl_data['Cumulative Strategy Return'], label='Strategy Return', alpha=0.75)
# plt.title("Cumulative Returns")
# plt.legend()
# plt.show()

total_strategy_return = aapl_data['Cumulative Strategy Return'].iloc[-1] - 1
total_market_return = aapl_data['Cumulative Market Return'].iloc[-1] - 1

print(f"Total Strategy Return: {total_strategy_return:.2%}")
print(f"Total Market Return: {total_market_return:.2%}")