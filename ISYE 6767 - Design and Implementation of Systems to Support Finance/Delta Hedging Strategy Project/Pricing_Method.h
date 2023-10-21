#ifndef PRICING_METHOD_H
#define PRICING_METHOD_H
#include <utility>
#include "Option.h"

using namespace std;

class Pricing_Method
{
public:
    virtual pair<double, double> BSM_Option_Price_Delta(const Option &option) const = 0;

    // Virtual destructor
    virtual ~Pricing_Method();
};

#endif
