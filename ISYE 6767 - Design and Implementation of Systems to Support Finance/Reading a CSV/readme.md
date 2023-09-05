How to run my code:
Software - Requirements:
To run my code correctly you will require the following software components:
1. A Linux Terminal (it can be a native linux OS, but i have used WSL on Windows)
2. g++ compiler (version: g++-11 (Ubuntu 11.1.0-1ubuntu1~20.04) 11.1.0)
3. make (version: GNU Make 4.2.1)

Commads to run my code:

Since i have used make there are only two steps to run my code
1. open up a termnial in the directory that has this code and has make installe and type in make
2. then run ./homework_1 (to run the compiled binary)

Alternatively (if you dont have make installed) you can simply run
1. g++ homework_1.cpp -o homework_1
2. ./homework_1

if you want to re-compile the code usisng make run
1. make clean
2. make

This removes the previous binary and then re-compile the code to produce a new binary

Input: This program reads a csv that has MOODY'S YIELD ON SEASONED CORPORATE BONDS - BAA along with the corersponding date for the yield and the date in the input here
Output: The corresponding bond yield for a date and the difference between the yield and the mean of the dataset is printed

Functions implemented in this code
There are 3 functions that i have implemented along with the main function i will explain each one of them in a top down fashion
1. bool is_valid_date(string date)
2. double average(vector<double> v)
3. double find_rate(vector<double> rate_vec, vector<string> date_vec, string date)


Firstly, bool is_valid_date(string date)
This function validates the date that the user has entered, the pupose of this function to do input validation so that program
can pre-emptively determine malformed inputs and inputs that will return no data since they are out of range for the dataset
that we have loaded, this ensures that compute cylces are not wasted in lookingup the data in a vector which takes O(N) time.

if the date entered is between 1919-01 and 2013-07 it is valid input any deviations to this pattern including not giving the date
in a YYYY-MM format or not using a '-' as delimiter between Year and month or flipping the Year and month or an invalid month will 
all return false only the valid date when parsed through this function will return true


Secondly, double average(vector<double> v)
This function simply calculates the average of the bond yield vector and returns it, to compute the average
i have used the accumulate() from the <numeric> class and it returns the sum and i divide it by the size of
the vector to get the average.


Thidly, double find_rate(vector<double> rate_vec, vector<string> date_vec, string date)
This function iterates through the date_vec to find the input date that the user has entered 
and then it gives us the index of the input date within the date_vec and we can use the same
index value to find the yield of the bond for the given date in the rate_vec

Instead of using the traditional for loop to iterate through the vector, I've employed the range-based for loop introduced in C++11. I've also utilized the auto keyword, which allows the compiler to automatically infer the type of the iterator for the vector.


Finally, the main() function
It first loads the csv() into the memory and parses it  and skips over the first 6 rows of data as they contain headers and other meta-data
which are not really that helpful for our computation, then it enters an infinite while loop expecting the user to enter dates in YYYY-MM format
once a date is entered it validates the date using the is_valid_date() method and if returns true, it will lookup the rate using teh find_rate function
and also compute the average and stores it in a variable and retunrs both the rate and difference between the rate and the average.

The while loop terminates when the appropriate ctrl + d or any other EOF command dependnig on the OS is sent.