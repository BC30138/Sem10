#ifndef _OPENMPALG_H_
#define _OPENMPALG_H_
#include "../tools/TridiagonalSLE.h"
using namespace std;

class OpenMPalg : public TridiagonalSLE{
  public:
    OpenMPalg(): TridiagonalSLE() {}
    OpenMPalg(unsigned long len_of_middle):  TridiagonalSLE(len_of_middle) { }
    void solve(int thread_num);  
};

#endif