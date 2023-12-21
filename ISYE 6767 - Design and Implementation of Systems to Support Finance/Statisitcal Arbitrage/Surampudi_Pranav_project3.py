import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tqdm import tqdm
import statsmodels.api as sm
from sklearn.decomposition import PCA
import matplotlib.dates as mdates
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objs as go
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import QuantLib as ql
class StatisticalArbitrage:
    # Formating the Datetime Column in the two Datasets
    def convert_dt_time(self):
        self.crypto_data['startTime'] = pd.to_datetime(self.crypto_data['startTime'])
        self.top_crypto['startTime'] = pd.to_datetime(self.top_crypto['startTime'])

    def save_trading_signals_to_disk(self):
        self.trading_signals_df.to_csv("trading_signal.csv")

    def save_eigen_vec_to_disk(self):
        self.eigenportfolio1_weights.to_csv('task1a_1.csv')
        self.eigenportfolio2_weights.to_csv('task1a_2.csv')

    def plot_eigen_portfolio(self):
        plot_date_range = [pd.Timestamp('2021-09-26 12:00:00+00:00'), pd.Timestamp('2022-04-15 20:00:00+00:00')]
        axes = plt.subplots(1, 2, figsize=(20, 8))
        for i, date in enumerate(plot_date_range):
            eigenportfolio1_weights_date = self.eigenportfolio1_weights.loc[date]
            eigenportfolio2_weights_date = self.eigenportfolio2_weights.loc[date]
            # Sort by eigenportfolio1 weights in descending order of absolute values
            s_indexes = eigenportfolio1_weights_date.abs().sort_values(ascending=False).index
            eigenportfolio1_weights_sorted = eigenportfolio1_weights_date.loc[s_indexes].abs() / self.eigen_scale
            eigenportfolio2_weights_sorted = eigenportfolio2_weights_date.loc[s_indexes].abs() / self.eigen_scale
            # Plotting both eigenportfolio weights
            axes[i].plot(eigenportfolio1_weights_sorted, linestyle='-', marker='o', label='Eigenportfolio 1')
            axes[i].plot(eigenportfolio2_weights_sorted, linestyle='-', marker='x', label='Eigenportfolio 2')
            # Set titles, labels, and grid
            axes[i].set_title(f'Eigenportfolio Weights on {date}')
            axes[i].set_xlabel('Ticker')
            axes[i].set_ylabel('Weight')
            axes[i].tick_params(axis='x', rotation=90)
            axes[i].legend()
            # Adding both x and y grid lines
            axes[i].grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.show()
    def plot_cr(self):
        btc_eth = self.crypto_data[(self.crypto_data['startTime'] >= self.testing_begin) & (self.crypto_data['startTime'] <= self.testing_end)][['startTime', 'BTC', 'ETH']]
        returns = btc_eth.set_index('startTime').pct_change()
        mean_returns = returns.mean()
        std_returns = returns.std()
        std_returns = ((returns - mean_returns) / std_returns).fillna(0)
        plt.figure(figsize=(20, 8))
        for token in std_returns.columns:
            plt.plot(std_returns.index, std_returns[token].cumsum(), label=token)
        for key in self.cr:
            plt.plot(self.cr[key].index, np.cumsum(self.cr[key]) / self.RET_SCALE, label=f'Cumulative {key}')
        plt.legend()
        plt.title('Cumulative Returns of Eigenportfolios, BTC, ETH, and Standardized Token Returns')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Return (%)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    def draw_s_score(self):
        # Plotting s-score for BTC
        plt.figure(figsize=(20, 8))
        plt.plot(self.btc_s_scores.index, np.cumsum(self.btc_s_scores) / 100, 
                 label='BTC s-score', color='red', linewidth=2, linestyle='--', marker='o')
        plt.title('Evolution of Cumulative s-score for BTC', fontsize=16)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Cumulative s-score', fontsize=14)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='-.', linewidth=0.5)
        plt.tight_layout()
        plt.show()
        # Plotting s-score for ETH
        plt.figure(figsize=(20, 8))
        plt.plot(self.eth_s_scores.index, np.cumsum(self.eth_s_scores) / 100, 
                 label='ETH s-score', color='blue', linewidth=2, linestyle='--', marker='*')
        plt.title('Evolution of Cumulative s-score for ETH', fontsize=16)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Cumulative s-score', fontsize=14)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='-.', linewidth=0.5)
        plt.tight_layout()
        plt.show()
    # Method to plot the cumilative returns of the Trading Strategy and Histogram of Hourly Data Distribution
    def plot_metrics(self):
            # Plotting Cumulative Returns
            cr = (1 + self.portfolio_returns).cumprod() - 1
            plt.figure(figsize=(20, 8))
            plt.plot(cr, label='Cumulative Returns', color='deepskyblue', 
                     linewidth=2, linestyle='-', marker='o', markersize=4)
            plt.title('Cumulative Return of the Strategy', fontsize=16)
            plt.xlabel('Time:', fontsize=14)
            plt.ylabel('Cumulative Return', fontsize=14)
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.savefig('cumulative_return.png')  
            plt.show()
            # Histogram of Hourly Returns
            plt.figure(figsize=(20, 8))
            self.portfolio_returns.hist(bins=10000, alpha=0.7, color='steelblue', edgecolor='black')
            plt.title('Histogram of Hourly Returns', fontsize=16)
            plt.xlabel('Return(%)', fontsize=14)
            plt.ylabel('Frequency', fontsize=14)
            plt.xlim(-0.1, 0.1)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig('hist_return.png')
            plt.show()
    def compute_sharpe_mmd(self):
        # Sharpe Ratio considering the risk-free rate of 0%
            Sharpe_Ratio = self.portfolio_returns.mean() / self.portfolio_returns.std() * 252
        # Max Drawdown
            rolling_max = self.portfolio_value_df['Portfolio Value'].cummax()
            drawdown = (self.portfolio_value_df['Portfolio Value'] / rolling_max) - 1
            max_drawdown = drawdown.min()
            return Sharpe_Ratio, max_drawdown

    # Constructor for the Class, since most of the variables are static i have put them all here instead of passing them as parameters while creting the object
    def __init__(self,init_inv):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            self.eigen_scale = 500
            self.trading_signals_df = pd.DataFrame()
            self.eigenportfolio1_weights = pd.DataFrame()
            self.testing_end = pd.to_datetime('2022-09-25 23:00:00').tz_localize('UTC')
            self.start_date = '2021-09-26 00:00:00'
            self.top_crypto = pd.read_csv("coin_universe_150K_40.csv",low_memory = False)
            self.end_date = '2022-09-25 23:00:00'
            self.crypto_data = pd.read_csv("coin_all_prices_full.csv",low_memory = False)
            self.testing_begin = pd.to_datetime('2021-09-26 00:00:00').tz_localize('UTC')
            self.eth_s_scores = pd.Series(dtype='float64')
            self.btc_s_scores = pd.Series(dtype='float64')
            self.eigenportfolio2_weights = pd.DataFrame(dtype='float64')
            self.initial_investment = init_inv
            self.RET_SCALE = 10
            self.cr = {
                'eigen_portfolio_1': pd.Series(dtype='float64'),
                'eigen_portfolio_2': pd.Series(dtype='float64'),
            }
            self.convert_dt_time()
    # Filtering the Data, Performing PCA, Computing the eigen values, s_scores and building portfolios and generating trading signals
    def trading_strat(self):
        print("Running Trading Strat, this function will take time to execute")
        for current_time in tqdm(pd.date_range(start=self.testing_begin, end=self.testing_end, freq='h')):
            M = 240
            end_time = current_time - pd.Timedelta(hours=M)
            
            # Filter top 40 tokens
            top_40_tokens = self.top_crypto[(self.top_crypto['startTime'] >= end_time) & (self.top_crypto['startTime'] < current_time)]
            
            # Find common tokens with at least 80% presence in the time window
            common_tokens = top_40_tokens.iloc[:, 1:].melt()['value'].value_counts()
            common_tokens = common_tokens[common_tokens >= 0.8 * M].index.tolist()
            
            # Filter price data for these tokens and filling missing data using ffill
            price_data_for_common_crypto = self.crypto_data[(self.crypto_data['startTime'] > end_time) & (self.crypto_data['startTime'] <= current_time)][['startTime'] + common_tokens]
            price_data_for_common_crypto.ffill(inplace=True)
            
            # Calculate standardized returns
            returns = price_data_for_common_crypto.set_index('startTime').pct_change().dropna()
            mean_returns = returns.mean()
            std_returns = returns.std()
            std_returns = ((returns - mean_returns) / std_returns)
            
            # Calculate the empirical correlation matrix
            correlation_matrix = std_returns.corr().fillna(0)
            
            # Perform PCA analysis
            pca = PCA(n_components=2)
            pca.fit(correlation_matrix)
            eigenvalues = pca.explained_variance_
            eigenvectors = pca.components_
        
            # Construction of Eigenportfolios Q(1) and Q(2)
            eigenportfolio1 = eigenvectors[0] / std_returns
            eigenportfolio2 = eigenvectors[1] / std_returns
        
            self.eigenportfolio1_weights.loc[current_time, eigenportfolio1.index] = eigenportfolio1.values
            self.eigenportfolio2_weights.loc[current_time, eigenportfolio2.index] = eigenportfolio2.values
        
            # Calculation of Factor Returns 
            factor_returns_one = (eigenportfolio1 * returns).sum(axis=1)
            factor_returns_2 = (eigenportfolio2 * returns).sum(axis=1)
                
            self.cr['eigen_portfolio_1'][current_time] = factor_returns_one.loc[current_time]
            self.cr['eigen_portfolio_2'][current_time] = factor_returns_2.loc[current_time]
        
            deltas, beta_coeffs, X_L_series_data, ou_parameters,trading_signals = dict({}), dict({}), dict({}), dict({}),dict({}) 
            
            for token in common_tokens:
                y = returns[token]
                y.fillna(0, inplace=True)
                y.replace([np.inf, -np.inf], 0, inplace=True)
                X = sm.add_constant(pd.concat([factor_returns_one, factor_returns_2], axis=1))
                ols_regression = sm.OLS(y, X).fit()
                deltas[token] = ols_regression.resid
                beta_coeffs[token] = ols_regression.params
                
            
            for token in common_tokens:
                x_lower = deltas[token].cumsum()
                X_L_series_data[token] = x_lower.shift(1).dropna()
                y = x_lower.iloc[1:]
                X = sm.add_constant(X_L_series_data[token])
                model = sm.OLS(y, X).fit()
                
                alpha, beta = model.params
                ou_parameters[token] = {
                    'alpha': alpha,
                    'beta': beta,
                    'kappa': -np.log(beta) / (1/8760),  
                    'm': alpha / (1 - beta),
                    'sigma': np.sqrt(model.scale / (2 * -np.log(beta) * (1 - beta ** 2))),
                    'sigma__eq': np.sqrt(model.scale / (1 - beta ** 2))
                }
            # Set trading parameter values
            s_bo = 1.25  
            s_so = 1.25  
            s_bc = 0.75  
            s_sc = 0.50 
            for token in common_tokens:
                m = ou_parameters[token]['m']
                sigma__eq = ou_parameters[token]['sigma__eq']
                X_t = deltas[token].iloc[-1]
            
                # Calculate the s-score
                s_score = (X_t - m) / sigma__eq
        
                # Store s-scores for BTC and ETH
                if token == 'BTC':
                    self.btc_s_scores[current_time] = s_score
                elif token == 'ETH':
                    self.eth_s_scores[current_time] = s_score
            
                # Generate trading signals
                if s_score <= -s_bo:
                    signal = "Buy to Open"
                elif s_score >= s_so:
                    signal = "Sell to Open"
                elif s_score <= s_bc:
                    signal = "Close Short Position"
                elif s_score >= -s_sc:
                    signal = "Close Long Position"
                else:
                    signal = "Hold"
            
                trading_signals[token] = signal
        
            for token in trading_signals:
                self.trading_signals_df.loc[current_time, token] = trading_signals[token]

    def trade_and_compute_metrics(self):
        self.portfolio_value = self.initial_investment
        self.portfolio_holdings = {token: 0 for token in self.trading_signals_df.columns}
        self.portfolio_value_history = []
        self.crypto_data_data = self.crypto_data.set_index('startTime')

        for timestamp in self.trading_signals_df.index:
            for token in self.trading_signals_df.columns:
                signal = self.trading_signals_df.loc[timestamp, token]
                token_price = self.crypto_data_data.loc[timestamp, token]

                if signal == "Buy to Open":
                    self.portfolio_holdings[token] += 1  
                    self.portfolio_value -= token_price
                elif signal == "Sell to Open":
                    self.portfolio_holdings[token] -= 1  
                    self.portfolio_value += token_price

            # Calculate portfolio value at the current timestamp
            current_portfolio_value = sum(self.crypto_data_data.loc[timestamp, token] * holding 
                                          for token, holding in self.portfolio_holdings.items())
            current_portfolio_value += self.portfolio_value  
            self.portfolio_value_history.append(current_portfolio_value)

        # Constructing the Portfolio Dataframe
        self.portfolio_value_df = pd.DataFrame(self.portfolio_value_history, index=self.trading_signals_df.index, columns=['Portfolio Value'])
        self.portfolio_returns = self.portfolio_value_df.pct_change().fillna(0)['Portfolio Value']



def main():
    sa = StatisticalArbitrage(100000)
    sa.trading_strat()
    sa.save_eigen_vec_to_disk()
    sa.save_trading_signals_to_disk()
    sa.plot_eigen_portfolio()
    sa.plot_cr()
    sa.draw_s_score()
    sa.trade_and_compute_metrics()
    sa.plot_metrics()
    sr, md = sa.compute_sharpe_mmd()
    print("Sharpe Ratio:", sr)
    print("Maximum Drawdown:", md)


if __name__ == "__main__":
    main()