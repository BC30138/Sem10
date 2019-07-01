#include"MPIalg.h"
#include<mpi.h>
#include<string>
#include<fstream>

using namespace std;

unsigned long get_size() {
    ifstream params("src/MPI/MPIparams.data");
    string tmp;
    params >> tmp;
    string delimiter = "=";
    size_t pos = tmp.find(delimiter);
    tmp.erase(0, pos + 1);
    return strtoul(tmp.c_str(), NULL, 0);
}
void test_1(unsigned long n) {
    MPIalg test(n);
    ofstream out("data/MPItime.data", fstream::app);
    test.solve(true, out);
}

void test_2() {
    // test.export_data("data/test_matrix.data");
    MPIalg test;
    test.read_data("data/test_matrix.data");
    test.solve(false, cout);
    // test.show_result();
}

int main() {
    unsigned long n = get_size();
    // test_1(n);
    test_2();
    return 0;
}