#include<iostream>
#include <sstream>
#include<iomanip>
#include<vector>
#include"functions.h"

void print_vector(vector<double> vec, ostream& out) {
    out << setprecision(2) << fixed;
    for (auto it = vec.begin(); it != vec.end(); ++it)
        out << *it << ' ';
    out << "\n";
}

void print_vector(vector<int> vec, ostream& out) {
    out << setprecision(2) << fixed;
    for (auto it = vec.begin(); it != vec.end(); ++it)
        out << *it << ' ';
    out << "\n";
}

vector<double> string_to_d_vector(string str) {
    istringstream ss(str);
    vector<double> res;
    double d_tmp;
    while(ss >> d_tmp) {
        res.push_back(d_tmp);
    }
    return res;
}

vector<double> ThomasAlg(vector<double> b, vector<double> a, vector<double> c, vector<double> d) {
    unsigned long n = d.size();
    vector<double> alpha(n - 1);
    vector<double> beta(n - 1);
    vector<double> x(n);

    // прямой проход
    alpha[0] = - c[0] / a[0];
    beta[0] = d[0] / a[0];

    for (unsigned long it = 1; it < n - 1; it ++) {
        double y = a[it] + b[it - 1] * alpha[it - 1];
        alpha[it] = - c[it] / y;
        beta[it] = (d[it] - b[it - 1] * beta[it - 1]) / y;
    }

    // обратный проход
    x[n - 1] = (d[n - 1] - b[n - 2] * beta[n - 2]) /
                (a[n - 1] + b[n - 2] * alpha[n - 2]);

    for (int it = n - 2; it >= 0; it--) {
        x[it] = alpha[it] * x[it + 1] + beta[it];
    }

    return x;
}

vector<double> get_subvector(vector<double> vec, int begin, int end) {
    vector<double>::const_iterator first = vec.begin() + begin;
    vector<double>::const_iterator last = vec.begin() + end;
    vector<double> sub_vec(first, last);
    return sub_vec;
}