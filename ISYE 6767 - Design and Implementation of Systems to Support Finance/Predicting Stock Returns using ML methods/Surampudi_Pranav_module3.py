import warnings
# Suppress all UserWarning warnings
warnings.simplefilter("ignore", category=UserWarning)
import backtrader as bt
import yfinance as yf
import numpy as np
import pyfolio as pf
import quantstats
import matplotlib.pyplot as plt
import pandas as pd
def reports(sd,ed,pred,ticker,model):
    # Load historical data for RHI from Yahoo Finance
    start_date = sd
    end_date = ed
    data_tgt = yf.download(ticker, start=start_date, end=end_date,progress=False)


    y_pred = pred

    # Define the trading strategy based on random predictions
    class MLBasedStrategy(bt.Strategy):
        def __init__(self):
            self.counter = 0

        def next(self):
            if self.counter < len(y_pred):
                if y_pred[self.counter] == 0:
                    self.buy()
                else:
                    self.close()
            self.counter += 1

    # Initialize Cerebro engine
    cerebro = bt.Cerebro()

    # Set initial cash and commission
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.05)

    # Add strategy
    cerebro.addstrategy(MLBasedStrategy)

    # Add data feed
    data_feed = bt.feeds.PandasData(dataname=data_tgt)
    cerebro.adddata(data_feed)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    # Run the strategy
    results = cerebro.run()

    # Extract results for PyFolio
    strategy = results[0]
    pyfoliozer = strategy.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    # Ensure the returns are a pandas Series
    returns = pd.Series(returns)

    # Check if returns, positions, or transactions are empty
    if returns.empty or positions.empty or transactions.empty:
        print("One or more of the required data structures (returns, positions, transactions) are empty.")

    # Quantstats report
    if returns.empty:
        print("No returns data available for quantstats.")
    else:
        try:
            quantstats.reports.html(returns, title=f"{model} Based Strategy Report for {ticker}", output=f'{ticker}-{model}-quantstats_report.html')
        except Exception as e:
            print(f"Error creating quantstats report: {e}")
