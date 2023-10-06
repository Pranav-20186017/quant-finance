# Option Pricing Toolkit

## Overview
This project offers a toolkit to compute the option prices and their respective deltas using two methods: the Black-Scholes-Merton (BSM) model and the Binomial model. The pricing is designed to support both call and put options. 

A significant improvement was made in the BSM model calculations. Originally, a polynomial approximation of the standard normal was used, which led to a discrepancy of around 0.90-1 in the option's value when compared with theoretical values from online calculators and other libraries. To address this, the standard normal from the Boost library was employed, leading to more accurate results.

## Files Description:

### 1. main.cpp
- Primary entry point of the application.
- Offers an interface for users to input the parameters for the option they want to evaluate.
- Conducts a series of unit tests to verify the correctness of the implemented models.

### 2. Option.cpp & Option.h
- Define the `Option` class which acts as a blueprint for any financial option.
- Store key parameters like the type of option (call or put), strike price, initial stock price, risk-free rate, time to maturity, and volatility.
- Offer methods to retrieve and set these parameters.

### 3. Option_Price.cpp & Option_Price.h
- Define the `Option_Price` class which inherits from the `Option` class.
- Incorporate the pricing methods - BSM and Binomial.
- Compute both the option price and its delta using the respective models.

### 4. Pricing_Method.h
- An interface that the `Option_Price` class implements.
- Ensures that any class implementing it would have methods for computing both the option price and its delta.

### 5. StdNormalCDF.cpp
- Provides an implementation for computing the Cumulative Distribution Function (CDF) of the standard normal distribution.
- Mainly used in the BSM model calculations.

### 6. test.cpp & test.h
- Dedicated to unit testing.
- Ensure that given a set of known parameters, the computed option prices and deltas match the expected values closely.

## Requirements:
- **g++ version:** g++-11 (Ubuntu 11.1.0-1ubuntu1~20.04) 11.1.0
- **make version:** GNU Make 4.2.1 Built for x86_64-pc-linux-gnu
- **Boost library version:** 1.83.0

## How to Run:
1. Compile the project using the provided Makefile:
   make all
2. To run the code just run the main binary:
   ./main
