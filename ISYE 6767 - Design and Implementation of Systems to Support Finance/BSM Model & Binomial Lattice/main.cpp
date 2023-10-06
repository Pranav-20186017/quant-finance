#include <iostream>
#include "Option_Price.h"
#include <cassert>
#include "test.h"
using namespace std;

int main()
{
    std::cout << "Running unit tests...\n";
    runUnitTests();

    char flag;
    double K, S, r, T, sigma;
    int steps;

    std::cout << "Enter option type (c for call, p for put): ";
    std::cin >> flag;
    std::cout << "Enter strike price: ";
    std::cin >> K;
    std::cout << "Enter current price of underlying: ";
    std::cin >> S;
    std::cout << "Enter risk-free rate: ";
    std::cin >> r;
    std::cout << "Enter time to maturity: ";
    std::cin >> T;
    std::cout << "Enter volatility: ";
    std::cin >> sigma;
    std::cout << "Enter steps for binomial model: ";
    std::cin >> steps;

    Option_Price option(flag, K, S, r, T, sigma);
    option.setSteps(steps);

    std::cout << "BSM Price: " << option.BSM_Pricer() << "\n";
    std::cout << "BSM Delta: " << option.BSM_Delta() << "\n";
    std::cout << "Binomial Price: " << option.Binomial_Pricer() << "\n";
    std::cout << "Binomial Delta: " << option.Binomial_Delta() << "\n";

    return 0;
}
