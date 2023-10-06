
#include "Option.h"

// Private initialization function
void Option::init()
{
    K = 100.0;
    S = 100.0;
    r = 0.05;
    T = 1.0;
    sigma = 0.2;
}

// Default constructor - initializes with default values
Option::Option()
{
    init();
}

// Parameterized constructor
Option::Option(double KVal, double SVal, double rVal, double TVal, double sigmaVal)
    : K(KVal), S(SVal), r(rVal), T(TVal), sigma(sigmaVal) {}

// Destructor
Option::~Option() {}

// Getters for the option parameters
double Option::getK() const { return K; }
double Option::getS() const { return S; }
double Option::getR() const { return r; }
double Option::getT() const { return T; }
double Option::getSigma() const { return sigma; }
