import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier
import Surampudi_Pranav_module7
import Surampudi_Pranav_module4
import Surampudi_Pranav_module1
import Surampudi_Pranav_module5
import Surampudi_Pranav_module6
import argparse
import tempfile
import os
import backtrader as bt
class CustomCSVData(bt.feeds.GenericCSVData):
    # Adjust the 'dtformat' parameter based on your CSV file's date format
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('dtformat', ('%Y-%m-%d')),  # Adjust this format if your CSV includes time
    )

    def __init__(self):
        super().__init__()

    @classmethod
    def preprocess_data(cls, file_name, file_type):
        # Reading and preprocessing the CSV file
        # Adjust this part based on the actual format of your CSV files
        df = pd.read_csv(file_name, parse_dates=['Date'],
                         dayfirst=True if file_type != '002054.XSHE' else False,
                         header=None if file_type == '002054.XSHE' else 0,
                         names=['Date', 'open', 'close', 
                                'high', 'low', 'volume', 
                                'money', 'avg', 'high_limit', 
                                'low_limit', 'pre_close', 'paused', 
                                'factor'] if file_type == '002054.XSHE' else None,
                         skiprows=1 if file_type == '002054.XSHE' else 0)
        df.sort_values(by='Date', inplace=True)

        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
        df.to_csv(temp_file.name, index=False)
        return temp_file.name

class PrintDataStrategy(bt.Strategy):
    def __init__(self):
        self.bar_counter = 0

    def next(self):
        num_bars_to_print = 5
        if self.bar_counter < num_bars_to_print:
            print(self.data.datetime.date(0), self.data.open[0], 
                  self.data.high[0], self.data.low[0], 
                  self.data.close[0], self.data.volume[0])
            self.bar_counter += 1

def run_print(data):
    print("Date: Open: High: Low: Close: Volume:")
    cerebro = bt.Cerebro()
    cerebro.addstrategy(PrintDataStrategy)
    cerebro.adddata(data)
    cerebro.run()

def data_loader():
    # Running backtest for each dataset
    datasets = ['002054.XSHE','aapl', 'ERCOTDA_price']
    for dataset in datasets:
        file_name = f'./csv_data/{dataset}.csv'  # Ensure the file path is correct
        preprocessed_file = CustomCSVData.preprocess_data(file_name, dataset)
        data = CustomCSVData(dataname=preprocessed_file)
        run_print(data)
        os.remove(preprocessed_file) 


def main():
    parser = argparse.ArgumentParser(description='Process some commands.')
    parser.add_argument('command', choices=['train_su', 'train_bu', 'chart_su_SVM','chart_su_EXT','chart_bu_SVM'], help='The command to execute a function')
    args = parser.parse_args()
    if args.command == 'train_su':
        features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'OBV',
        'Standard_Deviation', 'ADX', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100',
        'SMA_200', 'EMA_10', 'EMA_20', 'EMA_50', 'Middle_BB', 'Upper_BB',
        'Lower_BB', 'RSI', 'MACD', 'Signal_Line', 'Volume_Change', 'Price_ROC',
        '%K', '%D', 'Return']
        # Define the columns of the dataframe
        columns = ['ticker', 'model', 'accuracy', 'precision', 'F1', 'AUC']
        # Initialize an empty dataframe with these columns
        metrics_df = pd.DataFrame(columns=columns)
        # Read the CSV file
        df = pd.read_csv('tickers.csv')
        # Convert the 'Ticker' column to a list
        tickers = df['Ticker'].tolist()
        for ticker in tickers:
            start_date = '2000-01-01'
            end_date = '2021-11-12'
            # Fetch the data
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            data.fillna(method='bfill',inplace=True)
            featured_data = Surampudi_Pranav_module1.feature_engieering(data)
            normalized_data = Surampudi_Pranav_module1.nomalize(featured_data)
            X = normalized_data[features]
            y = normalized_data['Target']
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.4, random_state=42)
            # Initialize Support Vector Machine classifier
            svm_model = SVC(probability=True)  # Enable probability estimates for AUC calculation

            # Fit the model
            svm_model.fit(X_train, y_train)

            # Make predictions
            y_pred = svm_model.predict(X_test)
            accuracy,precision,f1,auc = Surampudi_Pranav_module1.evaluate_model(svm_model,X_test,y_test,y_pred)
            # Creating a new row as a DataFrame
            new_row = pd.DataFrame({
                'ticker': [ticker], 
                'model': ["Suuport Vector Machine"], 
                'accuracy': [accuracy], 
                'precision': [precision], 
                'F1': [f1], 
                'AUC': [auc]
            })
            # Using concat to add the new row to the dataframe
            metrics_df = pd.concat([metrics_df, new_row], ignore_index=True)

            # Initialize the Extra Trees Classifier
            extra_trees_model = ExtraTreesClassifier(n_estimators=100, random_state=42)

            # Fit the model on your training data
            extra_trees_model.fit(X_train, y_train)

            # Predict on the test data
            y_pred = extra_trees_model.predict(X_test)
            accuracy,precision,f1,auc = Surampudi_Pranav_module1.evaluate_model(extra_trees_model,X_test,y_test,y_pred)
            # Creating a new row as a DataFrame
            new_row = pd.DataFrame({
                'ticker': [ticker], 
                'model': ["Extra Trees Classifier"], 
                'accuracy': [accuracy], 
                'precision': [precision], 
                'F1': [f1], 
                'AUC': [auc]
            })
            # Using concat to add the new row to the dataframe
            metrics_df = pd.concat([metrics_df, new_row], ignore_index=True)
            metrics_df.to_csv("Metrics_Small_Universe.csv")
    elif args.command == 'train_bu':
        Surampudi_Pranav_module7.run()
    elif args.command == 'chart_su_SVM':
        Surampudi_Pranav_module4.charting_SVM()
    elif args.command == 'chart_su_EXT':
        Surampudi_Pranav_module5.charting_EXT()
    elif args.command == 'chart_bu_SVM':
        Surampudi_Pranav_module6.charting_SVM()
if __name__ == "__main__":
    main()
