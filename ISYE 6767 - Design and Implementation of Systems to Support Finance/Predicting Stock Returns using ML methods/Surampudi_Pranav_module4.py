import warnings
# Suppress all UserWarning warnings
warnings.simplefilter("ignore", category=UserWarning)
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
import Surampudi_Pranav_module3
import Surampudi_Pranav_module1
def charting_SVM():
    features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'OBV',
       'Standard_Deviation', 'ADX', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100',
       'SMA_200', 'EMA_10', 'EMA_20', 'EMA_50', 'Middle_BB', 'Upper_BB',
       'Lower_BB', 'RSI', 'MACD', 'Signal_Line', 'Volume_Change', 'Price_ROC',
       '%K', '%D', 'Return']
    tickers = ['RHI','TGT']
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
        # Calculate the split point
        split_point = int(len(data) * 0.6)

        # Split the data into training and testing sets
        X_train = X.iloc[:split_point]
        X_test = X.iloc[split_point:]
        y_train = y.iloc[:split_point]
        y_test = y.iloc[split_point:]
        # Initialize Support Vector Machine classifier
        svm_model = SVC(probability=True)  # Enable probability estimates for AUC calculation

        # Fit the model
        svm_model.fit(X_train, y_train)

        # Make predictions
        y_pred = svm_model.predict(X_test)

        # If y_pred is a numpy array, convert it to a Pandas Series with the test data's date index
        y_pred = pd.Series(y_pred, index=y_test.index)
        sd,ed,pred = Surampudi_Pranav_module1.get_indices_and_series_as_array(y_pred)
        sd, ed = sd.split(' ')[0], ed.split(' ')[0]
        Surampudi_Pranav_module3.reports(sd,ed,pred,ticker,"SVM")
        

