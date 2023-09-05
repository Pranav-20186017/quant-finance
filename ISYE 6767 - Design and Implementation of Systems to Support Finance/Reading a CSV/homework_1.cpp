#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
using namespace std;

bool is_valid_date(string date)
{
   if (!(date.find("-") != string::npos))
   {
      cout << "Wrong Date Format use the delimiter '-' in YYYY-MM format" << endl;
      return false;
   }
   if (date.length() < 7 || date.length() > 7)
   {
      cout << "Incorrect Date, Please enter a correct date" << endl;
      return false;
   }

   string::size_type pos = date.find("-");

   if (pos != string::npos)
   {
      string year = date.substr(0, pos);
      string month = date.substr(pos + 1);
      if (year.length() != 4 || month.length() != 2)
      {
         cout << "Invalid Date, Please enter a correct date in the YYYY-MM format" << endl;
         return false;
      }
      int int_year = stoi(year);
      int int_month = stoi(month);
      if (int_year < 1919 || int_year > 2013)
      {
         cout << "Invalid Year, Please enter a Year in between 1919 and 2013 (inclusive of both years)" << endl;
         return false;
      }
      else if ((int_year == 1919 && int_month < 1) || (int_year == 2013 && int_month > 7))
      {
         cout << "Date Range out of dataset, Please enter a Date in between 1919-01 and 2013-07" << endl;
         return false;
      }

      else if (int_month <= 0 || int_month > 12)
      {
         cout << "Invalid Month, Please enter a month between 01 and 12" << endl;
         return false;
      }
   }
   return true;
}
double average(vector<double> v)
{
   // code for calculating average of members of v
   // and returning the average
   if (v.empty())
   {
      return 0.0;
   }
   // accumulate: Sums up the elements in a range [first, last).
   //    It takes three arguments: starting iterator, ending iterator, and an initial sum value.
   double sum = accumulate(v.begin(), v.end(), 0.0);
   // Here i am diving the sum with the size of the vector to compute the average
   double average = (sum) / v.size();
   return average;
}

double find_rate(vector<double> rate_vec, vector<string> date_vec, string date)
{
   // code for finding the Baa rate for the
   // given date (in yyyy-mm format)
   // and returning the rate for that month
   auto it = find(date_vec.begin(), date_vec.end(), date);

   if (it != date_vec.end())
   {
      int index = distance(date_vec.begin(), it);
      return rate_vec[index];
   }
   return 0.0;
}

int main()
{
   vector<double> rate;
   vector<string> date;
   ifstream infile("./hw1_H.15_Baa_Data.csv");

   // code for loading rate and date vectors from the file hw1_H.15_Baa_Data.csv
   // the headers should be handled properly. do not delete them manually
   string temp_line;
   for (int i = 0; i < 6; ++i)
   {
      getline(infile, temp_line); // Skip the first six lines (headers/metadata)
   }

   string data;
   while (getline(infile, data))
   {
      // Process each line as before, without the header
      string::size_type pos = data.find(","); // Find the position of the comma

      if (pos != string::npos)
      {
         string d = data.substr(0, pos);
         string r = data.substr(pos + 1);
         date.push_back(d);
         double rt = stod(r);
         rate.push_back(rt);
      }
   }

   infile.close();

   // code for prompting user for a date and returning the rate
   // and the difference between the rate for that date and the
   // average rate
   // run_tests();
   double avg = average(rate);
   while (true)
   {
      cout << "Enter a Date in the format YYYY-MM, include a - to seperate year and month: ";
      string inp_date;
      cin >> inp_date;
      if (is_valid_date(inp_date))
      {
         double lookup_rate = find_rate(rate, date, inp_date);
         if (lookup_rate == 0.0)
         {
            cout << "Rate not found in the dataset" << endl;
            continue;
         }
         cout << "Lookup rate: " << lookup_rate << endl;
         cout << "Difference: " << lookup_rate - avg << endl;
      }
   }

   // This code should allow the user to continue to input dates
   // until the user inputs the EOF (End-of-file), namely control-d (in linux/mac) or control-z (in windows)
   // This should not crash if a bad date is entered.

   return 0.0; // program end
}
