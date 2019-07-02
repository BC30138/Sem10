#include<iostream>
#include"../tools/TridiagonalSLE.h"
using namespace std;

int main() {
    TridiagonalSLE test(3);
    test.solve();
    test.show();

    return 0;
}