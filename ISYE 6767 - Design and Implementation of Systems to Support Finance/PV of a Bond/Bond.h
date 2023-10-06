#ifndef BOND_H
#define BOND_H
#include <iostream>
#include <string>
using namespace std;
class Bond
{
private:
    string expiration_date;
    double frequency, cupon_rate;

public:
    Bond();
    Bond(string exp, double frq, double cr);
    ~Bond();
    Bond(const Bond &);
    string ToString();
    double Price(double time_to_maturity, double interest_rate, double coupon_rate, double frequency, double face_value);
    double CalculateAveragePriceFrom2016To2020();
    bool RunUnitTests();
};
#endif