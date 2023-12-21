import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, roc_auc_score


def calculate_sma(df, period):
    return df['close'].rolling(window=period).mean()

def calculate_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    macd_line = df['close'].ewm(span=short_period, adjust=False).mean() - df['close'].ewm(span=long_period, adjust=False).mean()
    macd_signal = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, macd_signal

def calculate_roc(df, period=14):
    return ((df['close'] - df['close'].shift(period)) / df['close'].shift(period)) * 100

def calculate_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df['close'][i] > df['close'][i-1]:
            obv.append(obv[-1] + df['volume'][i])
        elif df['close'][i] < df['close'][i-1]:
            obv.append(obv[-1] - df['volume'][i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)

def calculate_mfi(df, period=14):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    raw_money_flow = typical_price * df['volume']
    positive_flow = []
    negative_flow = []
    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i-1]:
            positive_flow.append(raw_money_flow[i-1])
            negative_flow.append(0)
        elif typical_price[i] < typical_price[i-1]:
            negative_flow.append(raw_money_flow[i-1])
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)
            
    positive_mf = pd.Series(positive_flow).rolling(window=period).sum()
    negative_mf = pd.Series(negative_flow).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi

def calculate_standard_deviation(df, period=20):
    return df['close'].rolling(window=period).std()

def calculate_adx(df, period=14):
    df = df.copy()
    df['TR'] = np.maximum((df['high'] - df['low']), 
                          np.maximum(abs(df['high'] - df['close'].shift(1)), 
                                     abs(df['low'] - df['close'].shift(1))))
    
    df['+DM'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), 
                         np.maximum(df['high'] - df['high'].shift(1), 0), 0)
    df['-DM'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), 
                         np.maximum(df['low'].shift(1) - df['low'], 0), 0)
    
    df['TR14'] = df['TR'].rolling(window=period).sum()
    df['+DM14'] = df['+DM'].rolling(window=period).sum()
    df['-DM14'] = df['-DM'].rolling(window=period).sum()
    
    df['+DI14'] = 100 * (df['+DM14'] / df['TR14'])
    df['-DI14'] = 100 * (df['-DM14'] / df['TR14'])
    df['DX'] = 100 * abs(df['+DI14'] - df['-DI14']) / (df['+DI14'] + df['-DI14'])
    
    df['ADX'] = df['DX'].rolling(window=period).mean()
    
    return df['ADX']

def feature_engieering(data):
    # Calculate and add the On-Balance volume (OBV) to the DataFrame
    data['OBV'] = calculate_obv(data)

    # Calculate and add the Standard Deviation to the DataFrame to measure stock volatility
    data['Standard_Deviation'] = calculate_standard_deviation(data)

    # ADX
    data['ADX'] = calculate_adx(data)

    data['SMA_10'] = data['close'].rolling(window=10).mean()
    data['SMA_20'] = data['close'].rolling(window=20).mean()
    data['SMA_50'] = data['close'].rolling(window=50).mean()
    data['SMA_100'] = data['close'].rolling(window=100).mean()
    data['SMA_200'] = data['close'].rolling(window=100).mean()
    # Exponential Moving Average
    data['EMA_10'] = data['close'].ewm(span=10, adjust=False).mean()
    data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()
    data['EMA_50'] = data['close'].ewm(span=50, adjust=False).mean()

    # Bollinger Bands
    data['Middle_BB'] = data['close'].rolling(window=20).mean()
    data['Upper_BB'] = data['Middle_BB'] + 2*data['close'].rolling(window=20).std()
    data['lower_BB'] = data['Middle_BB'] - 2*data['close'].rolling(window=20).std()

    # Relative Strength Index (RSI)
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # MACD (Moving Average Convergence Divergence)
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    # volume Changes
    data['volume_Change'] = data['volume'].diff()

    # Price Rate of Change
    data['Price_ROC'] = data['close'].pct_change(periods=5)
    #Stochastic Oscillator
    k_window=14
    d_window=3
    low_min = data['low'].rolling(window=k_window).min()
    high_max = data['high'].rolling(window=k_window).max()
    data['%K'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
    # Calculate %D
    data['%D'] = data['%K'].rolling(window=d_window).mean()
    data['Return'] = data['close'].pct_change()
    data['Target'] = (data['Return']>0).astype(int)
    data.dropna(inplace = True)
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    return data

def nomalize(data):
    features = ['Open', 'high', 'low', 'close', 'Adj close', 'volume', 'OBV',
       'Standard_Deviation', 'ADX', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100',
       'SMA_200', 'EMA_10', 'EMA_20', 'EMA_50', 'Middle_BB', 'Upper_BB',
       'lower_BB', 'RSI', 'MACD', 'Signal_Line', 'volume_Change', 'Price_ROC',
       '%K', '%D', 'Return']
    scaler = MinMaxScaler(feature_range=(0,1))
    data[features] = scaler.fit_transform(data[features])
    return data

def evaluate_model(model,X_test,y_test,y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    return accuracy,precision,f1,auc


import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, roc_auc_score


def calculate_sma(df, period):
    return df['close'].rolling(window=period).mean()

def calculate_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    macd_line = df['close'].ewm(span=short_period, adjust=False).mean() - df['close'].ewm(span=long_period, adjust=False).mean()
    macd_signal = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, macd_signal

def calculate_roc(df, period=14):
    return ((df['close'] - df['close'].shift(period)) / df['close'].shift(period)) * 100

def calculate_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df['close'][i] > df['close'][i-1]:
            obv.append(obv[-1] + df['volume'][i])
        elif df['close'][i] < df['close'][i-1]:
            obv.append(obv[-1] - df['volume'][i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)

def calculate_mfi(df, period=14):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    raw_money_flow = typical_price * df['volume']
    positive_flow = []
    negative_flow = []
    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i-1]:
            positive_flow.append(raw_money_flow[i-1])
            negative_flow.append(0)
        elif typical_price[i] < typical_price[i-1]:
            negative_flow.append(raw_money_flow[i-1])
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)
            
    positive_mf = pd.Series(positive_flow).rolling(window=period).sum()
    negative_mf = pd.Series(negative_flow).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi

def calculate_standard_deviation(df, period=20):
    return df['close'].rolling(window=period).std()

def calculate_adx(df, period=14):
    df = df.copy()
    df['TR'] = np.maximum((df['high'] - df['low']), 
                          np.maximum(abs(df['high'] - df['close'].shift(1)), 
                                     abs(df['low'] - df['close'].shift(1))))
    
    df['+DM'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), 
                         np.maximum(df['high'] - df['high'].shift(1), 0), 0)
    df['-DM'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), 
                         np.maximum(df['low'].shift(1) - df['low'], 0), 0)
    
    df['TR14'] = df['TR'].rolling(window=period).sum()
    df['+DM14'] = df['+DM'].rolling(window=period).sum()
    df['-DM14'] = df['-DM'].rolling(window=period).sum()
    
    df['+DI14'] = 100 * (df['+DM14'] / df['TR14'])
    df['-DI14'] = 100 * (df['-DM14'] / df['TR14'])
    df['DX'] = 100 * abs(df['+DI14'] - df['-DI14']) / (df['+DI14'] + df['-DI14'])
    
    df['ADX'] = df['DX'].rolling(window=period).mean()
    
    return df['ADX']

def feature_engieering(data):
    # Calculate and add the On-Balance volume (OBV) to the DataFrame
    data['OBV'] = calculate_obv(data)

    # Calculate and add the Standard Deviation to the DataFrame to measure stock volatility
    data['Standard_Deviation'] = calculate_standard_deviation(data)

    # ADX
    data['ADX'] = calculate_adx(data)

    data['SMA_10'] = data['close'].rolling(window=10).mean()
    data['SMA_20'] = data['close'].rolling(window=20).mean()
    data['SMA_50'] = data['close'].rolling(window=50).mean()
    data['SMA_100'] = data['close'].rolling(window=100).mean()
    data['SMA_200'] = data['close'].rolling(window=100).mean()
    # Exponential Moving Average
    data['EMA_10'] = data['close'].ewm(span=10, adjust=False).mean()
    data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()
    data['EMA_50'] = data['close'].ewm(span=50, adjust=False).mean()

    # Bollinger Bands
    data['Middle_BB'] = data['close'].rolling(window=20).mean()
    data['Upper_BB'] = data['Middle_BB'] + 2*data['close'].rolling(window=20).std()
    data['lower_BB'] = data['Middle_BB'] - 2*data['close'].rolling(window=20).std()

    # Relative Strength Index (RSI)
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # MACD (Moving Average Convergence Divergence)
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    # volume Changes
    data['volume_Change'] = data['volume'].diff()

    # Price Rate of Change
    data['Price_ROC'] = data['close'].pct_change(periods=5)
    #Stochastic Oscillator
    k_window=14
    d_window=3
    low_min = data['low'].rolling(window=k_window).min()
    high_max = data['high'].rolling(window=k_window).max()
    data['%K'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
    # Calculate %D
    data['%D'] = data['%K'].rolling(window=d_window).mean()
    data['Return'] = data['close'].pct_change()
    data['Target'] = (data['Return']>0).astype(int)
    data.dropna(inplace = True)
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    return data

def nomalize(data):
    features = ['open', 'high', 'low', 'close', 'volume', 'OBV',
       'Standard_Deviation', 'ADX', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100',
       'SMA_200', 'EMA_10', 'EMA_20', 'EMA_50', 'Middle_BB', 'Upper_BB',
       'lower_BB', 'RSI', 'MACD', 'Signal_Line', 'volume_Change', 'Price_ROC',
       '%K', '%D', 'Return']
    scaler = MinMaxScaler(feature_range=(0,1))
    data[features] = scaler.fit_transform(data[features])
    return data

def evaluate_model(model,X_test,y_test,y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    return accuracy,precision,f1,auc


def get_indices_and_series_as_array(series):
    """
    Return the first and last index of a Pandas Series as strings and 
    the entire series as a NumPy array.

    Parameters:
    series (pd.Series): A pandas Series.

    Returns:
    tuple: A tuple containing first index as a string, last index as a string, 
           and the series as a numpy array.
    """
    if series.empty:
        return "", "", np.array([])
    
    first_index = str(series.index[0])
    last_index = str(series.index[-1])
    series_array = series.to_numpy()

    return first_index, last_index, series_array