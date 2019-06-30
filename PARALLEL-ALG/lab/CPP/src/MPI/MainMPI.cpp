#include"MPIalg.h"
#include<fstream>
#include<ctime> 

using namespace std;

void test_1(unsigned long n) {
    PthreadsAlg test(n);

    ofstream out("data/MPItime.data");
    out << "size: " << n << endl;
    out << "threads_num\t" << "time(s)" << endl;
    for (int threads_it = 1; threads_it < 8; threads_it++) {
        clock_t start = clock();
        test.solve(threads_it);
        out << threads_it << "\t" << (clock() - start) / (double)CLOCKS_PER_SEC << endl;
    }
}

void test_2(int threads) {
    // test.export_data("data/test_matrix.data");
    PthreadsAlg test;
    test.read_data("data/test_matrix.data");
    test.solve(threads);
    test.show_result();
}

int main() {
    unsigned long n = 3500000;
    test_1(n);
    // test_2(2);
    return 0;
}