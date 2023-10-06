#include "Option_Price.h"
#include <cmath>
#include "StdNormalCDF.h"
#include <boost/math/distributions/normal.hpp>
Option_Price::Option_Price(char optFlag, double KVal, double SVal, double rVal, double TVal, double sigmaVal)
    : Option(KVal, SVal, rVal, TVal, sigmaVal), flag(optFlag) {}

double Option_Price::BSM_Pricer()
{
    StdNormalCDF std_cdf;
    boost::math::normal_distribution<> standard_normal;
    double d1 = (log(getS() / getK()) + (getR() + (getSigma() * getSigma()) / 2) * getT()) / (getSigma() * sqrt(getT()));
    double d2 = d1 - getSigma() * sqrt(getT());

    if (flag == 'c' || flag == 'C')
    {
        return getS() * boost::math::cdf(standard_normal, d1) - getK() * exp(-getR() * getT()) * boost::math::cdf(standard_normal, d2);
    }
    else
    {
        return getK() * exp(-getR() * getT()) * boost::math::cdf(standard_normal, -d2) - getS() * boost::math::cdf(standard_normal, -d1);
    }
}

double Option_Price::BSM_Delta()
{
    StdNormalCDF std_cdf;
    boost::math::normal_distribution<> standard_normal;
    double d1 = (log(getS() / getK()) + (getR() + (getSigma() * getSigma()) / 2) * getT()) / (getSigma() * sqrt(getT()));
    if (flag == 'c' || flag == 'C')
    {
        return boost::math::cdf(standard_normal, d1);
    }
    else
    {
        return boost::math::cdf(standard_normal, d1) - 1;
    }
}

double Option_Price::Binomial_Pricer()
{
    int steps = getSteps();
    double dt = getT() / steps;
    double discount = exp(-getR() * dt);

    // u and d factors
    double u = exp(getSigma() * sqrt(dt));
    double d = 1 / u;

    // Risk-neutral probability
    double q = (exp(getR() * dt) - d) / (u - d);

    // Vector for storing stock prices and option values
    std::vector<double> stockPrices(steps + 1);
    std::vector<double> values(steps + 1);

    // Stock price tree initialization
    for (int i = 0; i <= steps; i++)
    {
        stockPrices[i] = getS() * pow(u, steps - i) * pow(d, i);
        if (flag == 'c' || flag == 'C')
            values[i] = std::max(0.0, stockPrices[i] - getK());
        else
            values[i] = std::max(0.0, getK() - stockPrices[i]);
    }

    // Backward recursion for option price
    for (int step = steps - 1; step >= 0; --step)
    {
        for (int i = 0; i <= step; i++)
        {
            values[i] = (q * values[i] + (1 - q) * values[i + 1]) * discount;
        }
    }
    return values[0];
}

// double Option_Price::Binomial_Delta()
// {
//     int steps = getSteps();
//     double dt = getT() / steps;
//     double discount = exp(-getR() * dt);

//     double u = exp(getSigma() * sqrt(dt));
//     double d = 1 / u;

//     double q = (exp(getR() * dt) - d) / (u - d);

//     std::vector<double> stockPrices(steps + 1);
//     std::vector<double> values(steps + 1);

//     for (int i = 0; i <= steps; i++)
//     {
//         stockPrices[i] = getS() * pow(u, steps - i) * pow(d, i);
//         if (flag == 'c' || flag == 'C')
//             values[i] = std::max(0.0, stockPrices[i] - getK());
//         else
//             values[i] = std::max(0.0, getK() - stockPrices[i]);
//     }

//     for (int step = steps - 1; step >= 0; --step)
//     {
//         for (int i = 0; i <= step; i++)
//         {
//             values[i] = (q * values[i] + (1 - q) * values[i + 1]) * discount;
//         }
//     }

//     // Delta calculation
//     double value_up = values[0];
//     double value_down = values[1];
//     double delta = (value_up - value_down) / (getS() * (u - d));

//     return delta;
// }

double Option_Price::Binomial_Delta()
{
    int steps = getSteps();
    double dt = getT() / steps;
    double discount = exp(-getR() * dt);

    double u = exp(getSigma() * sqrt(dt));
    double d = 1 / u;
    double q = (exp(getR() * dt) - d) / (u - d);

    // Calculate the stock price after one up and one down move
    double stockPriceUp = getS() * u;
    double stockPriceDown = getS() * d;

    // Initialize vectors for option values at each node for up and down movements
    std::vector<double> valuesUp(steps + 1);
    std::vector<double> valuesDown(steps + 1);

    // Calculate terminal option values for up move
    for (int i = 0; i <= steps; i++)
    {
        double terminalStockPrice = stockPriceUp * pow(u, steps - i) * pow(d, i);
        if (flag == 'c' || flag == 'C')
            valuesUp[i] = std::max(0.0, terminalStockPrice - getK());
        else
            valuesUp[i] = std::max(0.0, getK() - terminalStockPrice);
    }

    // Calculate terminal option values for down move
    for (int i = 0; i <= steps; i++)
    {
        double terminalStockPrice = stockPriceDown * pow(u, steps - i) * pow(d, i);
        if (flag == 'c' || flag == 'C')
            valuesDown[i] = std::max(0.0, terminalStockPrice - getK());
        else
            valuesDown[i] = std::max(0.0, getK() - terminalStockPrice);
    }

    // Backward induction for up move
    for (int step = steps - 1; step >= 0; --step)
    {
        for (int i = 0; i <= step; i++)
        {
            valuesUp[i] = (q * valuesUp[i] + (1 - q) * valuesUp[i + 1]) * discount;
        }
    }

    // Backward induction for down move
    for (int step = steps - 1; step >= 0; --step)
    {
        for (int i = 0; i <= step; i++)
        {
            valuesDown[i] = (q * valuesDown[i] + (1 - q) * valuesDown[i + 1]) * discount;
        }
    }

    // Delta calculation
    double valueUp = valuesUp[0];
    double valueDown = valuesDown[0];
    double delta = (valueUp - valueDown) / (getS() * (u - d));

    return delta;
}
