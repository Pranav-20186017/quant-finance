#include <boost/math/distributions/normal.hpp>
#include <iostream>
#include "Pricing_Method.h"
#include <cmath>
#include "Option_Price.h"
#include <vector>
using namespace std;

Option_Price::Option_Price(double strike, double spot, double rate, double maturity, double sigma, char optFlag)
    : Option(strike, spot, rate, maturity, sigma), flag(optFlag) {}

double Option_Price::N(double x) const
{
    boost::math::normal_distribution<> standard_normal;
    return boost::math::cdf(standard_normal, x);
}

pair<double, double> Option_Price::BSM_Option_Price_Delta(const Option &option) const
{
    // Pricing using the BSM Model
    double K = option.getStrike();
    double S = option.getSpot();
    double r = option.getRate();
    double T = option.getMaturity();
    double sigma = option.getVol();

    double d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T));
    double d2 = d1 - sigma * sqrt(T);

    if (flag == 'C' || flag == 'c')
    {
        double price = S * N(d1) - K * exp(-r * T) * N(d2);
        double delta = N(d1);
        return make_pair(price, delta);
    }
    else if (flag == 'P' || flag == 'p')
    {
        double price = K * exp(-r * T) * N(-d2) - S * N(-d1);
        double delta = N(d1) - 1;
        return make_pair(price, delta);
    }
    return make_pair(0, 0);
}

Option_Price::~Option_Price()
{
}
