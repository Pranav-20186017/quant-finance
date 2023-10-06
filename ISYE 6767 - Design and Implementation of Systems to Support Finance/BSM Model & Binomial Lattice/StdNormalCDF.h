#ifndef STDNORMALCDF_H
#define STDNORMALCDF_H

#include <iostream>
#include <vector>
using namespace std;
class StdNormalCDF
{
public:
    static const double a1, a2, a3, a4, a5, p;
    double Cdf_Calculator(double);
    vector<double> Cdf_vec_Calculator(vector<double>);
};

#endif // STDNORMALCDF_H
