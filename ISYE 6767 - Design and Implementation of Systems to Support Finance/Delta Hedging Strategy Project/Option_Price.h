#ifndef OPTION_PRICE_H
#define OPTION_PRICE_H

#include "Option.h"
#include "Pricing_Method.h"

class Option_Price : public Option, public Pricing_Method
{
public:
    char flag; // C for call P for put

    // Constructor
    Option_Price(double strike, double spot, double rate, double maturity, double volatility, char optionFlag);

    // BSM Pricer
    std::pair<double, double> BSM_Option_Price_Delta(const Option &option) const override;

    // Normal distribution function
    double N(double x) const;

    // Destructor
    virtual ~Option_Price();
};

#endif
