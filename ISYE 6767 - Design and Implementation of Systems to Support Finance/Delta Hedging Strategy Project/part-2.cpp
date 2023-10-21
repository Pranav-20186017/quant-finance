#include <boost/math/distributions/normal.hpp>
#include <string>
#include <sstream>
#include "part-2.h"
#include <cmath>
#include <fstream>

using namespace std;
void DeltaHedging::read_csv()
{
    string line, word, date;
    // Reading interest rate file
    fstream irfile("./data/interest.csv", ios::in);
    if (irfile.is_open())
    {
        while (getline(irfile, line))
        {
            stringstream stream(line);
            getline(stream, date, ',');
            getline(stream, word, ',');
            if (date == "date")
                continue;
            ir_date.push_back(date);
            ir_rate.push_back(stod(word) / 100.0);
        }
    }
    irfile.close();
    // Reading Stock price file
    fstream prfile("./data/sec_GOOG.csv", ios::in);
    if (prfile.is_open())
    {
        while (getline(prfile, line))
        {
            stringstream stream(line);
            getline(stream, date, ',');
            getline(stream, word, ',');
            if (date == "date")
                continue;
            google_date.push_back(date);
            google_rate.push_back(stod(word));
        }
    }
    prfile.close();

    // Reading Stock price file
    fstream opfile("./data/op_GOOG.csv", ios::in);
    string exdate, cp_flag, strike_price, best_bid, best_offer;
    if (opfile.is_open())
    {
        while (getline(opfile, line))
        {
            stringstream stream(line);
            getline(stream, date, ',');
            getline(stream, exdate, ',');
            getline(stream, cp_flag, ',');
            getline(stream, strike_price, ',');
            getline(stream, best_bid, ',');
            getline(stream, best_offer, ',');

            if (date == "date")
                continue;
            if (exdate != "2011-09-17" || strike_price != "500" || cp_flag != "C")
                continue;
            op_date.push_back(date);
            op_exdate.push_back(exdate);
            op_flag.push_back(cp_flag);
            op_strike.push_back(stod(strike_price));
            op_price.push_back((stod(best_bid) + stod(best_offer)) / 2);
        }
    }
    opfile.close();
}
DeltaHedging::DeltaHedging(string T0, string TN, string _T, double _K)
{
    t0 = T0;
    tN = TN;
    T = _T;
    K = _K;
    read_csv();
    delta_hedging();
    write_to_csv();
}
DeltaHedging::~DeltaHedging()
{
}

double DeltaHedging::normal(double x)
{
    boost::math::normal_distribution<> standard_normal;
    return boost::math::cdf(standard_normal, x);
}

pair<double, double> DeltaHedging::BSM_implied(double _K, double _T, double _r, double _S, double _sigma, char _flag)
{
    double d1 = (log(_S / _K) + (_r + (_sigma * _sigma) / 2) * _T) / (_sigma * sqrt(_T));
    double d2 = d1 - _sigma * sqrt(_T);

    if (_flag == 'c' || _flag == 'C')
    {
        double V = normal(d1) * _S - normal(d2) * _K * exp((-_r) * _T);
        double vega = _S * sqrt(_T) * normal(d1);
        return make_pair(V, vega);
    }
    else if (_flag == 'p' || _flag == 'P')
    {
        double value = normal(-d2) * K * exp(-_r * _T) - normal(-d1) * _S;
        double vega = _S * sqrt(_T) * normal(d1);
        return make_pair(value, vega);
    }
    return make_pair(-1.0, -1.0);
}

double DeltaHedging::get_stock_price(string date)
{
    for (int i = 0; i < google_date.size(); i++)
    {
        if (google_date[i] == date)
            return google_rate[i];
    }
    return -1.0;
}

int DeltaHedging::get_option_index(string date)
{
    for (int i = 0; i < op_date.size(); i++)
    {
        if (op_date[i] == date)
            return i;
    }
    return -1;
}
double DeltaHedging::get_interest_rate(string date)
{
    for (int i = 0; i < ir_date.size(); i++)
    {
        if (ir_date[i] == date)
            return ir_rate[i];
    }
    return -1.0;
}
// computing implied volatility using Netwon Raphson Method
double DeltaHedging::compute_implied_volatility(double price, double S0, double K, double T, double r, string flag)
{
    double sigma_0 = 1, sigma_1 = 0.5;
    auto output = BSM_implied(K, T, r, S0, sigma_0, flag[0]);
    double h = (output.first - price) / output.second;
    double EPSILON = 0.0001;
    while (abs(sigma_1 - sigma_0) > EPSILON)
    {
        sigma_0 = sigma_1;
        output = BSM_implied(K, T, r, S0, sigma_0, flag[0]);
        h = (output.first - price) / output.second;
        sigma_1 = abs(sigma_0 - h);
    }
    return sigma_1;
}

void DeltaHedging::delta_hedging()
{
    tm d0 = format_date(t0), tm0 = format_date(t0);
    tm d1 = format_date(tN);
    double price0;
    for (; mktime(&d0) <= mktime(&d1); ++d0.tm_mday)
    {
        string date = getString(d0);
        // Stock data
        double S = get_stock_price(date);
        if (S == -1)
            continue;
        // Option data
        int option_index = get_option_index(date);
        if (option_index == -1)
            continue;
        double o_strike = op_strike[option_index];
        double o_price = op_price[option_index];
        if (getString(d0) == getString(tm0))
            price0 = o_price;
        string o_flag = op_flag[option_index];
        string o_ex = op_exdate[option_index];
        double r = get_interest_rate(date);

        double seconds_per_day = 3600 * 24.0;
        auto Tex = format_date(T);

        double ttm = compute_days(d0, Tex) / 252.0;

        double sigma = compute_implied_volatility(o_price, S, o_strike, ttm, r, o_flag);

        double delta = BSM_Delta(o_strike, ttm, r, S, sigma, o_flag[0]);

        double pnl = price0 - o_price;

        output_date.push_back(date);
        output_stock.push_back(S);
        output_option_value.push_back(o_price);
        output_volatality.push_back(sigma);
        output_delta.push_back(delta);
        output_pnl.push_back(pnl);
    }
    double Bi = output_option_value[0] - output_delta[0] * output_stock[0];
    vector<double> B;
    output_Hedging_Error.push_back(0.0);
    output_pnl_hedge.push_back(0);
    B.push_back(Bi);
    for (int i = 1; i < output_date.size(); i++)
    {
        Bi = output_delta[i - 1] * output_stock[i] + B[i - 1] * exp(get_interest_rate(output_date[i]) / 252) - output_delta[i] * output_stock[i];
        B.push_back(Bi);
        double HE = output_delta[i - 1] * output_stock[i] + B[i - 1] * exp(get_interest_rate(output_date[i]) / 252) - output_option_value[i];
        output_Hedging_Error.push_back(HE);
        output_pnl_hedge.push_back(HE);
    }
    vector<double> temp = output_Hedging_Error;
    for (int i = 1; i < output_Hedging_Error.size(); i++)
    {
        output_Hedging_Error[i] = output_Hedging_Error[i] - temp[i - 1];
    }
    return;
}

void DeltaHedging::write_to_csv()
{
    std::ofstream results_fptr;
    results_fptr.open("./output/result.csv", ios::trunc);
    results_fptr << "Date,Stock Price,Value,Implied Vol,Delta,Hedging Error,PNL,PNL with Hedge\n";
    for (int i = 0; i < output_date.size(); i++)
    {
        string row = output_date[i] + "," + to_string(output_stock[i]) + "," + to_string(output_option_value[i]) + "," + to_string(output_volatality[i]) + "," + to_string(output_delta[i]) + "," + to_string(output_Hedging_Error[i]) + "," + to_string(output_pnl[i]) + "," + to_string(output_pnl_hedge[i]) + "\n";
        results_fptr << row;
    }
    results_fptr.close();
    return;
}

double DeltaHedging::compute_days(tm start, tm end)
{
    double count = 0.0;
    for (; mktime(&start) <= mktime(&end); ++start.tm_mday)
    {
        if (start.tm_wday == 0 || start.tm_wday == 6)
            continue;
        count = count + 1.0;
    }
    return count;
}

double DeltaHedging::BSM_Delta(double _K, double _T, double _r, double _S, double _sigma, char _flag)
{
    double d1 = (log(_S / _K) + (_r + (_sigma * _sigma) / 2) * _T) / (_sigma * sqrt(_T));
    double d2 = d1 - _sigma * sqrt(_T);
    double delta;
    if (_flag == 'c' || _flag == 'C')
    {
        delta = normal(d1);
    }
    else if (_flag == 'p' || _flag == 'P')
    {
        delta = normal(d1) - 1;
    }

    return delta;
}

tm DeltaHedging::format_date(int year, int month, int day)
{
    std::tm tm = {0};
    tm.tm_year = year - 1900;
    tm.tm_mon = month - 1;
    tm.tm_mday = day;
    return tm;
}

tm DeltaHedging::format_date(string date)
{
    int y, m, d;
    sscanf(date.c_str(), "%d-%d-%d", &y, &m, &d);
    return format_date(y, m, d);
}

string DeltaHedging::getString(tm dt)
{
    char mon[3], day[3];
    snprintf(mon, sizeof(mon), "%02d", dt.tm_mon + 1);
    snprintf(day, sizeof(day), "%02d", dt.tm_mday);
    return to_string(dt.tm_year + 1900) + "-" + string(mon) + "-" + string(day);
}