import yfinance as yf
import pandas as pd

# Define the tickers for Bitcoin, NIFTY 50, and S&P 500
tickers = ["BTC-USD", "^NSEI", "^GSPC"]

# Download data for all tickers
data = yf.download(tickers, start="2014-01-01", end="2023-12-31")

# Create a DataFrame that contains the closing prices of each asset
combined_data = pd.DataFrame({
    'BTC-USD': data['Close']['BTC-USD'],
    'NIFTY': data['Close']['^NSEI'],
})

# Calculate the correlation matrix
correlation_matrix = combined_data.corr()

# Print the correlation matrix
print(correlation_matrix)