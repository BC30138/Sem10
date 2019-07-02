#include"OpenMPalg.h"
#include<fstream>
#include<ctime>

using namespace std;

unsigned long get_size() {
    ifstream params("data/MPIparams.data");
    string tmp;
    params >> tmp;
    string delimiter = "=";
    size_t pos = tmp.find(delimiter);
    tmp.erase(0, pos + 1);
    return strtoul(tmp.c_str(), NULL, 0);
}

void test_1(unsigned long n) {
    OpenMPalg test(n);

    ofstream out("data/OMPtime.data");
    out << "size: " << n << endl;
    out << "threads_num\t" << "time(s)" << endl;
    for (int threads_it = 1; threads_it < 24; threads_it++) {
        clock_t start = clock();
        test.solve(threads_it);
        out << threads_it << "\t" << (clock() - start) / (double)CLOCKS_PER_SEC << endl;
    }
}

void test_2(int threads) {
    // test.export_data("data/test_matrix.data");
    OpenMPalg test;
    test.read_data("data/test_matrix.data");
    test.solve(threads);
    test.show_result();
}

int main() {
    unsigned long n = get_size();
    test_1(n);
    // test_2(2);
    return 0;
}