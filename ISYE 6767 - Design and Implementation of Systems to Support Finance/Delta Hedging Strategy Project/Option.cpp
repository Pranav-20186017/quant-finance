#include "Option.h"

// Option class
void Option::init(double strike, double spot, double rate, double maturity, double volatility)
{
    K = strike;
    S = spot;
    r = rate;
    T = maturity;
    sigma = volatility;
}

double Option::getStrike() const { return K; }
double Option::getSpot() const { return S; }
double Option::getRate() const { return r; }
double Option::getMaturity() const { return T; }
double Option::getVol() const { return sigma; }

Option::~Option() {}
Option::Option(double strike, double spot, double rate, double maturity, double volatility)
{
    init(strike, spot, rate, maturity, volatility);
}
Option::Option() { init(0.0, 0.0, 0.0, 0.0, 0.0); }
