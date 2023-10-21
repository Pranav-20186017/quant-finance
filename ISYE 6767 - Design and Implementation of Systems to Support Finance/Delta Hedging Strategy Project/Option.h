#ifndef OPTION_H
#define OPTION_H

class Option
{
private:
    void init(double strike, double underlying, double rate, double maturity, double sigma); // Init Method
    double K;                                                                                // Strike price
    double S;                                                                                // Current price of underlying
    double r;                                                                                // Risk free rate
    double T;                                                                                // Time to maturity
    double sigma;                                                                            // Volatility

public:
    // Constructors and Destructor
    Option();                                                                             // Default constructor
    Option(double strike, double underlying, double rate, double maturity, double sigma); // Constructor with all parameters as arguments
    ~Option();                                                                            // Destructor

    // Get() method for each of the parameters
    double getStrike() const;
    double getSpot() const;
    double getRate() const;
    double getMaturity() const;
    double getVol() const;
};

#endif
