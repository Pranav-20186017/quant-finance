#ifndef OPTION_PRICE_H
#define OPTION_PRICE_H

#include "Option.h"
#include "Pricing_Method.h"
#include "StdNormalCDF.h"

class Option_Price : public Option, public Pricing_Method
{
private:
    char flag; // 'c' for call, 'p' for put
    int steps;

public:
    Option_Price(char optFlag, double KVal, double SVal, double rVal, double TVal, double sigmaVal);

    // Overrides for virtual functions
    double BSM_Pricer() override;
    double BSM_Delta() override; // Computes the Delta value based on Black-Scholes-Merton’s option pricing formula
    double Binomial_Pricer() override;
    double Binomial_Delta() override;
    void setSteps(int s) { steps = s; }
    int getSteps() const { return steps; }
};

#endif
