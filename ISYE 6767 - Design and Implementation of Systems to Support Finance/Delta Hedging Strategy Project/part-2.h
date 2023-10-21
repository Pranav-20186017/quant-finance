#ifndef PART_II
#define PART_II
#include <string>
#include "Option_Price.h"
#include <vector>
#include <ctime>
#include <iostream>
using namespace std;

class DeltaHedging
{
protected:
    vector<string> op_date;
    vector<string> google_date;
    double K;
    vector<double> google_rate;
    vector<string> op_flag;
    vector<double> ir_rate;
    vector<double> op_strike;
    string t0;
    vector<string> op_exdate;
    string T;
    vector<string> ir_date;
    string tN;
    vector<double> op_price;

    // Output vectors
    vector<double> output_Hedging_Error;
    vector<double> output_delta;
    vector<double> output_stock;
    vector<string> output_date;
    vector<double> output_option_value;
    vector<double> output_pnl_hedge;
    vector<double> output_volatality;
    vector<double> output_pnl;

    pair<double, double> BSM_implied(double _K, double _T, double _r, double _S, double _sigma, char _flag);
    double normal(double x);
    tm format_date(int year, int month, int day);
    tm format_date(string date);
    double get_stock_price(string date);
    int get_option_index(string date);
    double get_interest_rate(string date);
    string getString(tm dt);
    double compute_days(tm start, tm end);
    void write_to_csv();
    void read_csv();

public:
    DeltaHedging(string T0, string TN, string _T, double _K);
    double compute_implied_volatility(double price, double S0, double K, double T, double r, string flag);
    double BSM_Delta(double _K, double _T, double _r, double _S, double _sigma, char _flag);
    ~DeltaHedging();
    void delta_hedging();
};
#endif
