
#include "Bond.h"
#include <iostream>
using namespace std;
int main()
{
    Bond bb;
    if (!bb.RunUnitTests())
    {
        std::cout << "Unit tests failed. Halting execution." << std::endl;
        return 1;
    }
    Bond b;
    cout << b.ToString() << endl;
    Bond b2("11-19-2035", 0.5, 7);
    cout << b2.ToString() << endl;
    Bond b3(b2);
    cout << b3.ToString() << endl;
    Bond b4;
    double bond_price = b4.Price(4.2, 0.07, 0.08, 0.5, 100.0);
    cout << bond_price << endl;
    Bond b5;
    double gross_earnings = b5.CalculateAveragePriceFrom2016To2020();
    double net_earnings = 98 - gross_earnings;
    if (net_earnings > 0)
    {
        cout << "This is a good Investment with a net earnings of " << net_earnings << "and gross earnings of " << gross_earnings << endl;
    }
    else
    {
        cout << "This is not a good investment" << endl;
    }
    return 0;
}
