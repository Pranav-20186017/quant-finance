#ifndef PRICING_METHOD_H
#define PRICING_METHOD_H

class Pricing_Method
{
public:
    // Pure virtual functions making this class abstract
    virtual double BSM_Pricer() = 0; // Compute European option price using BSM
    virtual double BSM_Delta() = 0;  // Compute Delta value of the option using BSM

    virtual double Binomial_Pricer() = 0; // Compute European option price using binomial lattice method
    virtual double Binomial_Delta() = 0;  // Compute Delta value of the option using binomial lattice method

    virtual ~Pricing_Method() {} // Virtual destructor
};

#endif // PRICING_METHOD_H
