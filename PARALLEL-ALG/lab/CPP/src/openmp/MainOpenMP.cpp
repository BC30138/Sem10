#include"OpenMPalg.h"

using namespace std;

int main() {
    OpenMPalg test(20000000);
    // test.export_data("data/test_matrix.data");
    // test.read_data("data/test_matrix.data");
    test.solve(1);

    return 0;
}