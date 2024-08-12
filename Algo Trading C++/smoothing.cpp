// #include <iostream>
// #include <stdlib.h>
// using namespace std;
// static int nbins = 13;
// static double bins[13] = {0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99};
// void print_ROC(int n, double *signal_vals, double *returns, FILE *fp, double *work_signal, double *work_return)
// {
//     int i, k, ibin;
//     double win_above, win_below, lose_above, lose_below;
//     char msg[512], msg2[512];
//     for (i = 0; i < n; i++)
//     {
//         work_signal[i] = signal_vals[i];
//         work_return[i] = returns[i];
//     }
//     qsortds(0, n - 1, work_signal, work_return);
//     fprintf(fp, "\n\nProfit Factor above and below various thresholds");
//     fprintf(fp, "\n\nThreshold Frac Gtr/Eq Long Pf Short PF Frace Less Short Pf Long Pf");
//     for (ibin = 0; ibin < nbins; ibin++)
//     {
//         k = (int)(bins[ibin] * (n + 1)) - 1;
//         if (k < 0)
//             k = 0;
//         while (k > 0 && work_signal[k - 1] == work_signal[k])
//             --k;
//         if (k == 0 || k == nbins - 1)
//             continue;
//         win_above = win_below = lose_above = lose_below = 0.0;
//         for (i = 0; i < k; i++)
//         {
//             if (work_return[i] > 0.0)
//                 lose_below += work_return[i];
//             else
//                 win_below -= work_return[i];
//         }

//         for (i = k; i < n; i++)
//         {
//             if (work_return[i] > 0.0)
//                 win_above += work_return[i];
//             else
//                 lose_above -= work_return[i];
//         }

//         if (lose_above > 0.0)
//         {
//             sprintf_s(msg2, "%12.4lf", win_above / lose_above);
//             strcat_s(msg, msg2);
//         }
//         else
//             strcat_s(msg, " Inf ");
//         if (win_above > 0.0)
//         {
//             sprintf_s(msg2, "%12.4lf", lose_above / win_above);
//             strcat_s(msg, msg2);
//         }
//         else
//             strcat_s(msg, " Inf ");

//         sprintf_s(msg2, "%13.3lf", (double)k / (double)n);
//         strcat_s(msg, msg2);
//         if (lose_below > 0.0)
//         {
//             sprintf_s(msg2, "%12.4lf", win_below / lose_below);
//             strcat_s(msg, msg2);
//         }
//         else
//             strcat_s(msg, " Inf ");

//         if (win_below > 0.0)
//         {
//             sprintf_s(msg2, "%12.4lf", lose_below / win_below);
//             strcat_s(msg, msg2);
//         }
//         else
//             strcat_s(msg, " Inf ");
//         fprintf(fp, "\n%s", msg);
//     }
// }

#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <sstream>
#include <fstream>
using namespace std;

static const int nbins = 13;
static double bins[nbins] = {0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99};

// A helper function to sort based on work_signal, keeping pairs with work_return.
void sort_signal_and_return(int n, double *work_signal, double *work_return)
{
    vector<pair<double, double>> pairs(n);
    for (int i = 0; i < n; ++i)
    {
        pairs[i] = {work_signal[i], work_return[i]};
    }

    sort(pairs.begin(), pairs.end(), [](const auto &a, const auto &b)
         { return a.first < b.first; });

    for (int i = 0; i < n; ++i)
    {
        work_signal[i] = pairs[i].first;
        work_return[i] = pairs[i].second;
    }
}

void print_ROC(int n, double *signal_vals, double *returns, FILE *fp, double *work_signal, double *work_return)
{
    stringstream ss;
    for (int i = 0; i < n; i++)
    {
        work_signal[i] = signal_vals[i];
        work_return[i] = returns[i];
    }

    sort_signal_and_return(n, work_signal, work_return);

    fprintf(fp, "\n\nProfit Factor above and below various thresholds");
    fprintf(fp, "\n\nThreshold Frac Gtr/Eq Long Pf Short PF Frac Less Short Pf Long Pf");

    for (int ibin = 0; ibin < nbins; ibin++)
    {
        int k = static_cast<int>(bins[ibin] * (n + 1)) - 1;
        if (k < 0)
            k = 0;
        while (k > 0 && work_signal[k - 1] == work_signal[k])
            --k;
        if (k == 0 || k == nbins - 1)
            continue;

        double win_above = 0.0, win_below = 0.0, lose_above = 0.0, lose_below = 0.0;
        for (int i = 0; i < k; i++)
        {
            if (work_return[i] > 0.0)
                lose_below += work_return[i];
            else
                win_below -= work_return[i];
        }

        for (int i = k; i < n; i++)
        {
            if (work_return[i] > 0.0)
                win_above += work_return[i];
            else
                lose_above -= work_return[i];
        }

        ss.clear(); // Clear any error flags
        ss.str(""); // Clear content
        ss << "\n";
        if (lose_above > 0.0)
            ss << (win_above / lose_above) << " ";
        else
            ss << "Inf ";

        if (win_above > 0.0)
            ss << (lose_above / win_above) << " ";
        else
            ss << "Inf ";

        ss << static_cast<double>(k) / n << " ";

        if (lose_below > 0.0)
            ss << (win_below / lose_below) << " ";
        else
            ss << "Inf ";

        if (win_below > 0.0)
            ss << (lose_below / win_below);
        else
            ss << "Inf";

        fprintf(fp, "%s", ss.str().c_str());
    }
}

int main()
{
    int n = 100; // Number of elements
    double signal_vals[100], returns[100];
    double work_signal[100], work_return[100];

    // Generate synthetic data for demonstration
    for (int i = 0; i < n; ++i)
    {
        signal_vals[i] = static_cast<double>(rand()) / RAND_MAX;           // Random signal values in [0, 1]
        returns[i] = (static_cast<double>(rand()) / RAND_MAX) * 2.0 - 1.0; // Random returns in [-1, 1]
    }

    // Open a file to write the ROC analysis
    FILE *fp = fopen("ROC_analysis.txt", "w");
    if (!fp)
    {
        cerr << "Failed to open file for writing." << endl;
        return 1;
    }

    // Call the function to print the ROC analysis to the file
    print_ROC(n, signal_vals, returns, fp, work_signal, work_return);

    // Close the file
    fclose(fp);

    cout << "ROC analysis has been written to ROC_analysis.txt" << endl;

    return 0;
}