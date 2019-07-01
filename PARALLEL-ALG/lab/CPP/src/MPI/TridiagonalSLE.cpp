#include<vector>
#include<iostream>
#include <random>
#include<time.h>
#include<iomanip>
#include<fstream>
#include"../tools/functions.h"
#include"TridiagonalSLE.h"
using namespace std;

TridiagonalSLE::TridiagonalSLE() {
    b.resize(0);
    a.resize(0);
    c.resize(0);
    d.resize(0);
    x.resize(0);
    n = 0;
}

TridiagonalSLE::TridiagonalSLE(unsigned long len_of_middle) {
    generate_random_SLE(len_of_middle);
}

void TridiagonalSLE::generate_random_SLE(unsigned long len_of_middle) {
    double lower_bound = 0;
    double upper_bound = 10;
    n = len_of_middle;
    b.resize(n - 1);
    a.resize(n);
    c.resize(n - 1);
    d.resize(n);
    x.resize(n);

    uniform_real_distribution<double> unif(lower_bound,upper_bound);
    default_random_engine re;

    a[0] = unif(re);
    d[0] = unif(re);
    for(unsigned long it = 0; it < n - 1; it++) {
        b[it] = unif(re);
        c[it] = unif(re);
        a[it + 1] = unif(re);
        d[it + 1] = unif(re);
    }
}

void TridiagonalSLE::solve() {
    vector<double> alpha(n - 1);
    vector<double> beta(n - 1);

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

    for (long long it = n - 2; it >= 0; it--) {
        x[it] = alpha[it] * x[it + 1] + beta[it];
    }
}

void TridiagonalSLE::show() {
    export_to(cout);
}

unsigned long TridiagonalSLE::size() {
    return n;
}

vector<double> TridiagonalSLE::get_result() {
    return x;
}

void TridiagonalSLE::show_result() {
    print_vector(x, cout);
}

void TridiagonalSLE::export_data(string file_path) {
    ofstream out(file_path);
    export_to(out);
}

void TridiagonalSLE::export_to(ostream& out) {
    out << setprecision(2) << fixed;

    out << "size: " << n << "\n";
    out << "b: ";
    for (unsigned long it = 0; it < n - 1; it++) out << b[it] << "\t";
    out << "\n";
    out << "a: ";
    for (unsigned long it = 0; it < n; it++) out << a[it] << "\t";
    out << "\n";
    out << "c: ";
    for (unsigned long it = 0; it < n - 1; it++) out << c[it] << "\t";
    out << "\n";

    out << "matrix:\n";
    out << a[0] << "\t" << c[0] << "\t";
    for (unsigned long it = 2; it < n; it++) {
        out << "0" << "\t";
    }
    out << "\n";
    for (unsigned long it = 1; it < n - 1; it++) {
        for (unsigned long jt = 0; jt < it - 1; jt ++) {
            out << "0" << "\t";
        }
        out << b[it - 1] << "\t" << a[it] << "\t" << c[it] << "\t";
        for (unsigned long jt = it + 2; jt < n; jt++) {
            out << "0" << "\t";
        }
        out << "\n";
    }
    for (unsigned long it = 0; it < n - 2; it++) {
        out << "0" << "\t";
    }
    out << b[n - 2] << "\t" << a[n - 1] << "\n";

    out << "d: ";
    for (unsigned long it = 0; it < d.size(); it++) out << d[it] << "\t";
    out << "\n";
}

void TridiagonalSLE::read_data(string file_path) {
    ifstream in(file_path);
    string s_tmp;

    in >> s_tmp; // size:
    in >> n;

    in >> s_tmp; // b:
    getline(in, s_tmp); // line with b
    b = string_to_d_vector(s_tmp);

    in >> s_tmp; // a:
    getline(in, s_tmp); // line with a
    a = string_to_d_vector(s_tmp);

    in >> s_tmp; // c:
    getline(in, s_tmp); // line with c
    c = string_to_d_vector(s_tmp);
    for (unsigned long it = 0; it < n + 1; it++) {
        getline(in, s_tmp);
    }

    in >> s_tmp; // d:
    getline(in, s_tmp); // line with d
    d = string_to_d_vector(s_tmp);

    x.resize(n);
}