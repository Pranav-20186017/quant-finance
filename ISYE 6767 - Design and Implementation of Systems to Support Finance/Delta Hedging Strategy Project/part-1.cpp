#include <vector>
#include <cmath>
#include "part-1.h"
#include <random>
#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;
double generate_random()
{
    static random_device rd{};
    static mt19937 gen{rd()};
    static normal_distribution<> d{0, 1};
    return d(gen);
}

vector<double> simulate_stock_path(int N, double S0, double T, double mu, double sigma)
{
    double dt = T / N;
    vector<double> stock_prices;
    double S = S0;
    stock_prices.push_back(S);
    for (int i = 1; i <= N; ++i)
    {
        S = S + mu * S * dt + sigma * S * sqrt(dt) * generate_random();
        stock_prices.push_back(S);
    }
    ofstream stock_path_F("./output/stock_prices.csv", ios::app);
    for (const auto &price : stock_prices)
    {
        stock_path_F << fixed << setprecision(5) << price << ",";
    }
    stock_path_F << endl;
    stock_path_F.close();
    return stock_prices;
}

pair<vector<double>, vector<double>> simulate_option_prices_and_delta(int N, const vector<double> &stock_prices, double K, double T, double r, double sigma, char type)
{
    double dt = T / N;
    vector<double> option_prices;
    vector<double> delta;
    Option_Price optionOne(K, stock_prices[0], r, T, sigma, type);
    pair<double, double> featOne = optionOne.BSM_Option_Price_Delta(optionOne);
    option_prices.push_back(featOne.first);
    delta.push_back(featOne.second);
    for (int i = 1; i <= N; ++i)
    {
        Option_Price inputOptionNext(K, stock_prices[i], r, T - i * dt, sigma, 'C');
        pair<double, double> bsmResultNext = inputOptionNext.BSM_Option_Price_Delta(inputOptionNext);
        option_prices.push_back(bsmResultNext.first);
        delta.push_back(bsmResultNext.second);
    }
    ofstream optionFile("./output/option_prices.csv", ios::app);
    for (const auto &price : option_prices)
    {
        optionFile << fixed << setprecision(5) << price << ",";
    }
    optionFile << endl;
    optionFile.close();
    return {option_prices, delta};
}

vector<double> calculate_hedging_errors(int N, const vector<double> &stock_prices, const vector<double> &option_prices, const vector<double> &delta, double r, double dt)
{
    vector<double> hedging_errors(1, 0.0);
    double B = option_prices[0] - delta[0] * stock_prices[0];
    double prev_delta = delta[0];
    for (int i = 1; i <= N; ++i)
    {
        double h_e = prev_delta * stock_prices[i] + B * exp(r * dt) - option_prices[i];
        B = prev_delta * stock_prices[i] + B * exp(r * dt) - delta[i] * stock_prices[i];
        prev_delta = delta[i];
        hedging_errors.push_back(h_e);
    }
    return hedging_errors;
}

// Function to generate CSV file hedging errors
void generate_csv_hedging_errors(double totalCumulativeHE)
{
    ofstream cumulativeHedgingErrorFile("./output/cumulative_hedging_errors.csv", ios::app);
    cumulativeHedgingErrorFile << totalCumulativeHE << endl;
    cumulativeHedgingErrorFile.close();
}

// Function to run the simulation
void run_monte_carlo_simulation(int N, int numPaths, double S0, double T, double mu, double sigma, double r, double K, char type)
{
    double dt = T / N;
    for (int path = 0; path < numPaths; ++path)
    {
        vector<double> stock_prices = simulate_stock_path(N, S0, T, mu, sigma);
        auto [option_prices, delta] = simulate_option_prices_and_delta(N, stock_prices, K, T, r, sigma, type);
        vector<double> hedging_errors = calculate_hedging_errors(N, stock_prices, option_prices, delta, r, dt);

        double totalCumulativeHE = 0;
        for (const auto &HE : hedging_errors)
        {
            totalCumulativeHE += HE;
        }

        generate_csv_hedging_errors(totalCumulativeHE);
    }
}
