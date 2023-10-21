#include "unit_test_monte_carlo_simulation.h"
#include <vector>
#include "part-2.h"
#include <iomanip>
#include "unit_test_delta_hedging.h"
#include <fstream>
#include "part-1.h"
#include <iomanip>
using namespace std;
int main()
{
    // Initialize simulation parameters
    UnitTestSimulation uts = UnitTestSimulation();
    double S0 = uts.S0, K = uts.K, T = uts.T, mu = uts.mu, sigma = uts.sigma, r = uts.r, N = uts.N, numPaths = uts.numPaths;
    char type = uts.type;
    // Run the Monte Carlo simulation
    cout << "Running the Unit test for Stock Simulation" << endl;
    run_monte_carlo_simulation(N, numPaths, S0, T, mu, sigma, r, K, type);
    cout << "writing csv files to disk" << endl;

    cout << "Running Unit test for Delta Hedging Methods" << endl;
    UnitTestDeltaHedging utdh = UnitTestDeltaHedging();
    DeltaHedging dh = DeltaHedging(utdh.T0, utdh.TN, utdh.T, utdh.K);

    const int width = 20; // Set a constant width for each field

    cout << "************ Implied volatility computation ************" << endl;
    cout << left << setw(width) << "Strike:" << utdh.K << endl;
    cout << left << setw(width) << "Time to Maturity:" << utdh.Ttm << endl;
    cout << left << setw(width) << "Interest Rate:" << utdh.r << endl;
    cout << left << setw(width) << "Option Price:" << utdh.option_price << endl;
    cout << left << setw(width) << "Stock Price:" << utdh.S0 << endl;
    cout << left << setw(width) << "Type:" << utdh.flag << endl;
    cout << left << setw(width) << "Implied Volatility:" << dh.compute_implied_volatility(utdh.option_price, utdh.S0, utdh.K, utdh.Ttm, utdh.r, utdh.flag) << "\n";

    cout << "************ Delta computation ************" << endl;
    cout << left << setw(width) << "Strike:" << utdh.K << endl;
    cout << left << setw(width) << "Time to Maturity:" << utdh.Ttm << endl;
    cout << left << setw(width) << "Interest Rate:" << utdh.r << endl;
    cout << left << setw(width) << "Volatility:" << utdh.sigma << endl;
    cout << left << setw(width) << "Stock Price:" << utdh.S0 << endl;
    cout << left << setw(width) << "Type:" << utdh.flag << endl;
    cout << left << setw(width) << "Delta:" << dh.BSM_Delta(utdh.K, utdh.Ttm, utdh.r, utdh.S0, utdh.sigma, utdh.flag.c_str()[0]) << endl;

    cout << "Writing results.csv to disk" << endl;
    return 0;
}
