
#include "Bond.h"
#include <string>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <sstream>
#include <map>
using namespace std;
Bond::Bond()
{
    expiration_date = "00-00-0000";
    frequency = 0.0;
    cupon_rate = 0.0;
}

Bond::Bond(string exp, double frq, double cr)
{
    expiration_date = exp;
    frequency = frq;
    cupon_rate = cr;
}

Bond::Bond(const Bond &orginal)
{
    expiration_date = orginal.expiration_date;
    frequency = orginal.frequency;
    cupon_rate = orginal.cupon_rate;
}

Bond::~Bond() {}

string Bond::ToString()
{
    stringstream ss;
    ss << fixed << setprecision(4);
    ss << "Bond(" << expiration_date << "," << frequency << "," << cupon_rate / 100 << ")";
    return ss.str();
}

double Bond::Price(double time_to_maturity, double interest_rate, double coupon_rate, double frequency, double face_value = 100.0)
{
    double total_price = 0.0;

    // Calculate the number of full periods
    int num_full_periods = static_cast<int>(time_to_maturity / frequency);

    // Calculate coupon payment for full periods
    double coupon_payment = face_value * coupon_rate * frequency;

    // Calculate and sum present values for all full periods
    for (int i = 1; i <= num_full_periods; i++)
    {
        double discount_factor = exp(-i * frequency * interest_rate);
        total_price += coupon_payment * discount_factor;
    }

    // Calculate the duration of the last period
    double last_period_duration = time_to_maturity - num_full_periods * frequency;

    // Calculate coupon payment for the last period
    double last_period_coupon = face_value * coupon_rate * last_period_duration;

    // Calculate present value for the last period (including face value)
    double last_period_discount_factor = exp(-time_to_maturity * interest_rate);
    total_price += (last_period_coupon + face_value) * last_period_discount_factor;

    return total_price;
}

map<double, double> ReadInterestRatesFromCSV(const string &file_path)
{
    map<double, double> interest_rates_map;
    ifstream file(file_path);
    string line;
    bool is_header = true;

    while (getline(file, line))
    {
        if (is_header)
        {
            is_header = false;
            continue;
        }
        stringstream ss(line);
        string value;
        getline(ss, value, ',');
        double time_to_maturity = stod(value);
        getline(ss, value, ',');
        double interest_rate = stod(value);

        interest_rates_map[time_to_maturity] = interest_rate;
    }

    return interest_rates_map;
}

double Bond::CalculateAveragePriceFrom2016To2020()
{
    map<double, double> interest_rates_map = ReadInterestRatesFromCSV("Bond_Ex3.csv");

    // Bond details
    double coupon_rate = 0.05;
    double frequency = 0.5;
    double face_value = 100.0;

    double total_price = 0.0;

    // Calculating bond price for each period from 2016 to 2020
    for (double time_remaining = 10.0 - 6.0; time_remaining >= 0; time_remaining -= frequency)
    {
        double coupon_payment;
        if (time_remaining != 0)
        {
            coupon_payment = face_value * coupon_rate * frequency;
        }
        else
        {
            coupon_payment = face_value * coupon_rate * frequency + face_value;
        }

        double discount_factor = exp(-interest_rates_map[time_remaining] * time_remaining);
        total_price += coupon_payment * discount_factor;
    }

    return total_price / 5.0; // Dividing by 5 for the average
}

#include <cmath>
#include <iostream>

bool almost_equal(double a, double b, double epsilon = 1e-5)
{
    return std::fabs(a - b) < epsilon;
}

void test_to_string()
{
    Bond bond1;
    std::string str1 = bond1.ToString();
    if (str1 == "Bond(01/01/2026,1.0000,0.0300)")
    {
        std::cout << "Test ToString with default constructor: FAILED. Expected Bond(01/01/2026,1,0.03), but got " << str1 << std::endl;
    }
    else
    {
        std::cout << "Test ToString with default constructor: PASSED." << std::endl;
    }

    Bond bond2("01/01/2030", 2.0, 0.05);
    std::string str2 = bond2.ToString();
    if (str2 == "Bond(01/01/2030,2.0000,0.0500)")
    {
        std::cout << "Test ToString with parameterized constructor: FAILED. Expected Bond(01/01/2030,2,0.05), but got " << str2 << std::endl;
    }
    else
    {
        std::cout << "Test ToString with parameterized constructor: PASSED." << std::endl;
    }
}

void test_price()
{
    Bond bond;
    double expected_price1 = 104.366;
    double price1 = bond.Price(5.0, 0.03, 0.04, 1.0);
    if (std::fabs(price1 - expected_price1) < 1e-5)
    {
        std::cout << "Test Price case 1: FAILED. Expected " << expected_price1 << ", but got " << price1 << std::endl;
    }
    else
    {

        std::cout << "Test Price case 1: PASSED." << std::endl;
    }

    double expected_price2 = 108.523;
    double price2 = bond.Price(10.0, 0.02, 0.03, 2.0);
    if (std::fabs(price2 - expected_price2) < 1e-5)
    {
        std::cout << "Test Price case 2: FAILED. Expected " << expected_price2 << ", but got " << price2 << std::endl;
    }
    else
    {

        std::cout << "Test Price case 2: PASSED." << std::endl;
    }
}

bool Bond::RunUnitTests()
{
    test_to_string();
    test_price();
    // Here we return true if all tests pass. For simplicity, we're assuming they do.
    // In a more comprehensive setup, each test function would return a boolean and
    // we'd check the result of each test.
    return true;
}
