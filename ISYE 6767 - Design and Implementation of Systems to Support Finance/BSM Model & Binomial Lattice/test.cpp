#include <cassert>
#include "Option_Price.h"
#include <iostream>
using namespace std;
void runUnitTests()
{
    const double tolerance = 0.001; // Adjust as needed.

    // Test 1
    {
        Option_Price testOption('c', 140, 136, 0.02, 0.5, 0.3);
        testOption.setSteps(1000);
        assert(abs(testOption.BSM_Pricer() - 10.3408) < tolerance);
        assert(abs(testOption.BSM_Delta() - 0.506605) < tolerance);
        assert(abs(testOption.Binomial_Pricer() - 10.341) < tolerance);
        assert(abs(testOption.Binomial_Delta() - 0.506659) < tolerance);
    }

    // Test 2
    {
        Option_Price testOption('p', 140, 136, 0.02, 0.5, 0.3);
        testOption.setSteps(1000);
        assert(abs(testOption.BSM_Pricer() - 12.9478) < tolerance);
        assert(abs(testOption.BSM_Delta() - (-0.493395)) < tolerance);
        assert(abs(testOption.Binomial_Pricer() - 12.9479) < tolerance);
        assert(abs(testOption.Binomial_Delta() - (-0.493341)) < tolerance);
    }

    // Test 3
    {
        Option_Price testOption('c', 40, 100, 0.05, 0.375, 0.2);
        testOption.setSteps(1000);
        assert(abs(testOption.BSM_Pricer() - 60.743) < tolerance);
        assert(abs(testOption.BSM_Delta() - 1) < tolerance);
        assert(abs(testOption.Binomial_Pricer() - 60.743) < tolerance);
        assert(abs(testOption.Binomial_Delta() - 1) < tolerance);
    }

    // Test 4
    {
        Option_Price testOption('C', 67.70, 76.70, 0.04, 1, 0.3);
        testOption.setSteps(1000);
        assert(abs(testOption.BSM_Pricer() - 15.5092) < tolerance);
        assert(abs(testOption.BSM_Delta() - 0.757844) < tolerance);
        assert(abs(testOption.Binomial_Pricer() - 15.5108) < tolerance);
        assert(abs(testOption.Binomial_Delta() - 0.757838) < tolerance);
    }

    std::cout << "All unit tests passed!" << std::endl;
}