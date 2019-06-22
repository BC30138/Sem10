#include<vector>
#include<iostream>
#include <random>
using namespace std;

// vector<double>[3] generate() {

// }

vector<double> ThomasAlg(vector<double> b, vector<double> a, vector<double> c, vector<double> d) {
    int n = a.size();
    vector<double> x(n);
    vector<double> alpha(n - 1);
    vector<double> beta(n - 1);

    // прямой проход
    alpha[0] = - c[0] / a[0];
    beta[0] = d[0] / a[0];

    for (int it = 1; it < n - 1; it ++) {
        double y = a[it] + b[it - 1] * alpha[it - 1];
        alpha[it] = - c[it] / y;
        beta[it] = (d[it] - b[it - 1] * beta[it - 1]) / y;
    }

    // обратный проход
    x[n - 1] = (d[n - 1] - b[n - 2] * beta[n - 2]) / (a[n - 1] + b[n - 2] * alpha[n - 2]);

    for (int it = n - 2; it >= 0; it--) {
        x[it] = alpha[it] * x[it + 1] + beta[it];
    }

    return x;
}

void test() {
    srand(time(NULL));
    int n = 3;
    double lower_bound = 0;
    double upper_bound = 10;
    vector<double> b(n - 1);
    vector<double> a(n);
    vector<double> c(n - 1);
    vector<double> d(n);

    uniform_real_distribution<double> unif(lower_bound,upper_bound);
    default_random_engine re;

    a[0] = unif(re);
    d[0] = unif(re);
    for(int it = 0; it < n - 1; it++) {
        b[it] = unif(re);
        c[it] = unif(re);
        a[it + 1] = unif(re);
        d[it + 1] = unif(re);
    }

    vector<double> x = ThomasAlg(b ,a ,c ,d);

    cout << "b: ";

    for (int it = 0; it < b.size(); it++) {
        cout << b[it] << " ";
    }

    cout << "\n";

    cout << "a: ";

    for (int it = 0; it < a.size(); it++) {
        cout << a[it] << " ";
    }

    cout << "\n";

    cout << "c: ";

    for (int it = 0; it < c.size(); it++) {
        cout << c[it] << " ";
    }

    cout << "\n";

    cout << "d: ";

    for (int it = 0; it < d.size(); it++) {
        cout << d[it] << " ";
    }

    cout << "\n";

    cout << "x: ";

    for (int it = 0; it < x.size(); it++) {
        cout << x[it] << " ";
    }

    cout << "\n";
}
