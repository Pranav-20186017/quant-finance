#include "unit_test_delta_hedging.h"

using namespace std;

string UnitTestDeltaHedging::T0 = "2011-07-05";
string UnitTestDeltaHedging::TN = "2011-07-29";
string UnitTestDeltaHedging::T = "2011-09-17";
double UnitTestDeltaHedging::K = 500.0;
// Fields to test implied vol.
double UnitTestDeltaHedging::option_price = 150.346;
double UnitTestDeltaHedging::S0 = 640.0;
double UnitTestDeltaHedging::r = 0.05;
double UnitTestDeltaHedging::Ttm = 0.4;
string UnitTestDeltaHedging::flag = "C";
// Field to calculate delta
double UnitTestDeltaHedging::sigma = 0.2;
