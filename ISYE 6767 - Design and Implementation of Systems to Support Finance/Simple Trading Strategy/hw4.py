"""
Title: ISYE 6767 Homework 4
Author: Pranav Surampudi
Date: 06-11-2023
"""
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import random
import unittest

def trading_strategy(filename):
    # Read prices from the given CSV file. If the file is "aapl.csv", use pandas to read it.
    # Otherwise, use the csv module to read the file.
    if filename == "aapl.csv":
        df = pd.read_csv(filename)
        prices = df['Close'].to_numpy()  # Convert the 'Close' column to a numpy array
    else:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Read each row in the CSV and convert to float, skipping empty rows
            prices = [float(row[0]) for row in reader if row]

    n = len(prices)
    signals = np.zeros(n)
    positions = np.zeros(n)
    account_values = np.zeros(n)
    initial_account_value = 10000
    sh = 10
    max_position = sh * 2
    account_values[0] = initial_account_value
    w = initial_account_value

    for i in range(1, n):
        if i >= 2 and prices[i-2] < prices[i-1] < prices[i] and (positions[i-1] + sh) <= max_position:
            signals[i] = 1
            positions[i] = positions[i-1] + sh
            w -= sh * prices[i]
        elif i >= 1 and prices[i-1] > prices[i] and positions[i-1] > 0:
            signals[i] = -1
            w += positions[i-1] * prices[i]
            positions[i] = 0
        elif i == n-1 and positions[i-1] > 0:
            signals[i] = -1
            w += positions[i-1] * prices[i]
            positions[i] = 0
        else:
            positions[i] = positions[i-1]
        account_values[i] = w + positions[i] * prices[i]

    # Write the results to a new CSV file, naming it based on the input filename
    with open(f'trading_results-{filename.replace(".csv","")}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Prices", "Signals", "Positions", "Account Values"])
        for i in range(n):
            writer.writerow([prices[i], signals[i], positions[i], account_values[i]])

    # Calculate the profit or loss by subtracting the initial account value from the final value
    profit_or_loss = w - initial_account_value
    # Print the cumulative trading profit-and-loss
    print(f"Cumulative Trading Profit-and-Loss: ${profit_or_loss:.2f}")

    # Return the signals, positions, and account values arrays
    return signals, positions, account_values


def plot_cumulative_PnL(prices, positions, utname):
    """
    Plot the cumulative Profit & Loss (P&L) for a given set of stock prices and positions over time.

    Parameters:
    prices (array-like): The stock prices over time.
    positions (array-like): The held stock positions over time. Must be one less in length than prices due to np.diff usage.
    utname (str): The base name for the output plot image file.

    This function first calculates the daily P&L by taking the difference of consecutive stock prices,
    multiplied by the positions held before that day. It then computes the cumulative P&L by taking
    the running sum of the daily P&L values. The cumulative P&L is plotted against time to visualize
    the performance of the trading strategy over the period considered.
    """

    # Calculate the daily P&L by taking the difference in consecutive prices (np.diff)
    # and multiplying by the position held before the price change.
    daily_pnl = np.diff(prices) * positions[:-1]
    
    # Calculate the cumulative P&L by taking the running sum of daily P&L.
    # np.cumsum computes the cumulative sum of an array.
    cumulative_pnl = np.cumsum(daily_pnl)

    # Insert a 0 at the beginning of the cumulative P&L array to represent the value at day 0.
    cumulative_pnl = np.insert(cumulative_pnl, 0, 0)
    
    # Begin plotting the cumulative P&L.
    plt.figure(figsize=(10, 6))  # Set the size of the plot.
    plt.plot(cumulative_pnl, label='Cumulative P&L', color='blue')  # Plot the cumulative P&L with a label.
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)  # Draw a horizontal line at y=0 as a reference.
    
    # Add title and labels to the plot.
    plt.title('Cumulative Profit and Loss over Time')
    plt.xlabel('Days')
    plt.ylabel('Cumulative P&L ($)')

    # Add a legend to the plot to identify the plotted line.
    plt.legend()

    # Add a grid to the plot for better readability of values.
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Save the plot as a PNG image file with the given utname as part of the filename.
    plt.savefig(f"{utname}.png")




def min_initial_energy(maze):
    """
    Calculate the minimum initial energy required to traverse a maze from the top-left corner to the
    bottom-right corner without the energy going below 1 at any point.

    Parameters:
    maze (list or numpy.ndarray): A 2D array-like object where each cell has an energy value.

    Returns:
    int: The minimum initial energy required to traverse the maze successfully.
    """

    # Check if maze is a list, and convert it to a numpy array if so
    if isinstance(maze, list):
        maze = np.array(maze)

    # If maze is empty, return 0 as no energy is needed for an empty maze
    if maze.size == 0:
        return 0

    m, n = maze.shape  # Use the shape to get the number of rows and columns

    # Initialize the dynamic programming (DP) table with zeros. This DP table will help us store
    # the minimum energy required to reach each cell from the bottom-right corner backwards.
    dp = np.zeros((m, n), dtype=int)

    # The energy at the destination (bottom-right cell) should be at least 1 after considering
    # the maze value at that cell. If the maze value is positive, 1 energy point is enough.
    # Otherwise, we need more points to overcome the deficiency and still have 1 point remaining.
    dp[-1, -1] = max(1 - maze[-1, -1], 1)

    # Fill in the last row and the last column as base cases for the DP table.
    # Here, we only have one choice for movement (either up for the last column or left for the last row),
    # so we just need to make sure that we have enough energy to move to the next cell and keep at least 1 energy.
    for i in range(m - 2, -1, -1):
        dp[i, n - 1] = max(dp[i + 1, n - 1] - maze[i, n - 1], 1)
    for j in range(n - 2, -1, -1):
        dp[m - 1, j] = max(dp[m - 1, j + 1] - maze[m - 1, j], 1)

    # Fill in the rest of the DP table in a bottom-up fashion.
    # Each cell (i, j) depends on the cell to the right (i, j+1) and the cell below (i+1, j).
    # The minimum initial energy for cell (i, j) is the energy required to reach either of the two dependent cells
    # minus the energy at cell (i, j), ensuring that at least 1 energy point remains.
    for i in range(m - 2, -1, -1):
        for j in range(n - 2, -1, -1):
            min_maze_on_exit = min(dp[i + 1, j], dp[i, j + 1])
            dp[i, j] = max(min_maze_on_exit - maze[i, j], 1)

    # The top-left cell of the DP table contains the minimum initial energy required to start the maze
    # such that the energy level never drops below 1 throughout the traversal to the bottom-right cell.
    return dp[0, 0]




# Test cases using the unittest library
class TestMinInitialEnergy(unittest.TestCase):
    def test_case_1(self):
        maze = np.array([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 7)

    def test_case_2(self):
        maze = np.array([[0, -2], [-3, 4]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 3)

    def test_case_3(self):
        maze = np.array([[-2, 1], [2, -1]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 3)

    def test_case_4(self):
        maze = np.array([[-1, -2, 2], [-2, -3, -3], [-3, -3, 1]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 5)

    def test_case_5(self):
        maze = np.array([[0, 0], [0, 0]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 1)

    def test_case_6(self):
        maze = np.array([[-1, -2, -3], [-1, -2, -3], [-1, -2, -3]])
        result = min_initial_energy(maze)
        print(f"Minimum Energy required for {maze} is: {result}")
        self.assertEqual(result, 9)

def main():
    # 1. Test the function using the provided example prices
    example_prices = [100, 102, 104, 103, 101, 99, 100, 102, 104, 106, 107, 105]
    with open('example_prices.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for price in example_prices:
            writer.writerow([price])

    test_signals, test_positions, test_account_values = trading_strategy('example_prices.csv')
    plot_cumulative_PnL(example_prices, test_positions, "sample_case")

    # 2. Run the trading strategy on aapl.csv
    aapl_signals, aapl_positions, aapl_account_values = trading_strategy('aapl.csv')
    plot_cumulative_PnL(pd.read_csv('aapl.csv')['Close'].to_numpy(), aapl_positions,"unit_test_aapl")


    # 3. Instantiate a concrete example for unit testing
    unit_test_prices = [105, 103, 104, 103, 105, 107, 108, 109, 110, 112, 110, 108, 107, 106, 108]
    with open('unit_test_prices.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for price in unit_test_prices:
            writer.writerow([price])

    unit_test_signals, unit_test_positions, unit_test_account_values = trading_strategy('unit_test_prices.csv')
    plot_cumulative_PnL(unit_test_prices, unit_test_positions,"unit_test_concrete-2")


    # 4. Instantiate another concrete example for unit testing
    # Setting the seed for reproducibility
    random.seed(903948185)

    # Generate random prices
    random_prices_length = random.randint(20, 100)  # Random length between 20 and 50
    random_prices = [random.randint(1, 1000) for _ in range(random_prices_length)]

    # Save the random prices to a CSV file
    with open('unit_test_prices_random.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for price in random_prices:
            writer.writerow([price])
    unit_test_signals, unit_test_positions, unit_test_account_values = trading_strategy('unit_test_prices_random.csv')
    plot_cumulative_PnL(random_prices, unit_test_positions,"random_prices")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMinInitialEnergy)
    unittest.TextTestRunner(verbosity=2).run(suite)



if __name__ == "__main__":
    main()