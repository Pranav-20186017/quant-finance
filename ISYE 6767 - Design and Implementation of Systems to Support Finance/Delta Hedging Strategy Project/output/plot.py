import pandas as pd
import matplotlib.pyplot as plt

def plot_stock_paths():
    df_stock = pd.read_csv("stock_prices.csv", header=None)

    # Plot first 100 paths
    for i in range(100):
        plt.plot(df_stock.iloc[i], label=f"Path {i+1}" if i < 10 else "", linewidth=0.7)

    plt.title("Sample Stock Price Paths")
    plt.xlabel("Time Steps")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_option_prices():
    df_option = pd.read_csv("option_prices.csv", header=None)

    # Plot first 100 option price paths
    for i in range(100):
        plt.plot(df_option.iloc[i], label=f"Path {i+1}" if i < 10 else "", linewidth=0.7)

    plt.title("Option Prices for Sample Paths")
    plt.xlabel("Time Steps")
    plt.ylabel("Option Price")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_hedging_errors():
    df_errors = pd.read_csv("cumulative_hedging_errors.csv", header=None)
    plt.hist(df_errors[0], bins=50, edgecolor='k', alpha=0.7)
    plt.title("Distribution of Hedging Errors")
    plt.xlabel("Hedging Error")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_stock_paths()
    plot_option_prices()
    plot_hedging_errors()
