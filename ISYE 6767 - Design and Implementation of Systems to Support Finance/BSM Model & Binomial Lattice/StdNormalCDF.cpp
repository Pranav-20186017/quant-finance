#include <math.h>
#include <vector>
#include "StdNormalCDF.h"
using namespace std;
const double StdNormalCDF::a1 = 0.254829592;
const double StdNormalCDF::a2 = -0.284496736;
const double StdNormalCDF::a3 = 1.421413741;
const double StdNormalCDF::a4 = -1.453152027;
const double StdNormalCDF::a5 = 1.061405;
const double StdNormalCDF::p = 0.3275911;

double StdNormalCDF::Cdf_Calculator(double x)
{
    // Implement the standard normal function CDF
    bool neg = false;
    if (x < 0)
    {
        x *= -1;
        neg = true;
    }
    double z = 1 / (1 + (0.2316419 * x));
    double R_z = pow(z, 3) * ((z * ((a5 * z) + a4)) + a3) + z * ((a2 * z) + a1);
    double cdf = 1 - (((1 / sqrt(2 * M_PI)) * (exp(-1 * (pow(x, 2) / 2)))) * R_z);
    if (neg)
    {
        return 1 - cdf;
    }
    return cdf;
}

vector<double> StdNormalCDF::Cdf_vec_Calculator(vector<double> v)
{
    vector<double> output; // Vector to store the computed CDF values

    // Loop through each value in the input vector
    for (double x : v)
    {
        // Compute the CDF value using the Cdf_Calculator method
        double cdf_value = Cdf_Calculator(x);

        // Append the computed CDF value to the output vector
        output.push_back(cdf_value);
    }

    // Return the output vector containing the CDF values
    return output;
}
