import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier
from tqdm import tqdm
import os
import Surampudi_Pranav_module2

def run():
        features = ['open', 'high', 'low', 'close', 'volume', 'OBV',
        'Standard_Deviation', 'ADX', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100',
        'SMA_200', 'EMA_10', 'EMA_20', 'EMA_50', 'Middle_BB', 'Upper_BB',
        'lower_BB', 'RSI', 'MACD', 'Signal_Line', 'volume_Change', 'Price_ROC',
        '%K', '%D', 'Return']
        # Define the columns of the dataframe
        columns = ['ticker', 'model', 'accuracy', 'precision', 'F1', 'AUC']

        # Initialize an empty dataframe with these columns
        metrics_df = pd.DataFrame(columns=columns)
        
        # Path to the folder containing the CSV files
        folder_path = './stock_dfs'  # Replace with the actual path to your folder

        # List to hold the names of files without the .csv extension
        tickers = []

        # Loop through the directory
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                tickers.append(file)

        for ticker in tqdm(tickers):
            data = pd.read_csv(f"{folder_path}/{ticker}")
            data.fillna(method='bfill',inplace=True)
            try:
                featured_data = Surampudi_Pranav_module2.feature_engieering(data)
                normalized_data = Surampudi_Pranav_module2.nomalize(featured_data)
            except Exception:
                continue
            X = normalized_data[features]
            y = normalized_data['Target']
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.4, random_state=42)
            # Initialize Support Vector Machine classifier
            svm_model = SVC(probability=True)  # Enable probability estimates for AUC calculation
            try:
                # Fit the model
                svm_model.fit(X_train, y_train)
                # Make predictions
                y_pred = svm_model.predict(X_test)
                accuracy,precision,f1,auc = Surampudi_Pranav_module2.evaluate_model(svm_model,X_test,y_test,y_pred)
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
            except Exception:
                continue
            # Initialize the Extra Trees Classifier
            extra_trees_model = ExtraTreesClassifier(n_estimators=100, random_state=42)

            # Fit the model on your training data
            extra_trees_model.fit(X_train, y_train)

            # Predict on the test data
            y_pred = extra_trees_model.predict(X_test)
            accuracy,precision,f1,auc = Surampudi_Pranav_module2.evaluate_model(extra_trees_model,X_test,y_test,y_pred)
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

        
        metrics_df.to_csv("Metrics_Big_Universe.csv")

