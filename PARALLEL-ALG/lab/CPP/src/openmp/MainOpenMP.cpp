#include"OpenMPalg.h"
#include<fstream>
#include<ctime>

using namespace std;

int main() {
    unsigned long n = 13000000;
    OpenMPalg test(n);
    ofstream out("data/OMPtime.data");
    out << "size: " << n << endl;
    out << "threads_num\t" << "time(s)" << endl;
    // test.export_data("data/test_matrix.data");
    // test.read_data("data/test_matrix.data");
    for (int threads_it = 1; threads_it < 8; threads_it++) {
        clock_t start = clock();
        test.solve(1);
        out << threads_it << "\t" << (clock() - start) / (double)CLOCKS_PER_SEC << endl;
    }
    // test.show_result();

    return 0;
}