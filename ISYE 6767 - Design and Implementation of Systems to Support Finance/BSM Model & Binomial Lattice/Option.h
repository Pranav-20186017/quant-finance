
#ifndef OPTION_H
#define OPTION_H

class Option
{
private:
    double K;     // Strike price
    double S;     // Current price of underlying
    double r;     // Risk-free rate
    double T;     // Time to maturity
    double sigma; // Volatility

    void init(); // Initialize the option with default values

public:
    // Default constructor
    Option();

    // Parameterized constructor
    Option(double KVal, double SVal, double rVal, double TVal, double sigmaVal);

    // Destructor
    virtual ~Option();

    // Getters for the option parameters
    double getK() const;
    double getS() const;
    double getR() const;
    double getT() const;
    double getSigma() const;
};

#endif // OPTION_H
