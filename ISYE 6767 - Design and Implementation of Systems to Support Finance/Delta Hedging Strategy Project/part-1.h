#ifndef PART_I_H
#define PART_I_H

#include <vector>
#include <random>
#include <utility>
#include "Option_Price.h"

double generate_random();
std::vector<double> simulate_stock_path(int N, double S0, double T, double mu, double sigma, char type);
std::pair<std::vector<double>, std::vector<double>> simulate_option_prices_and_deltas(int N, const std::vector<double> &stockPrices, double K, double T, double r, double sigma);
std::vector<double> calculate_hedging_errors(int N, const std::vector<double> &stockPrices, const std::vector<double> &optionPrices, const std::vector<double> &deltas, double r, double dt);
void generate_csv_hedging_errors(double totalCumulativeHE);
void run_monte_carlo_simulation(int N, int numPaths, double S0, double T, double mu, double sigma, double r, double K, char type);

#endif
