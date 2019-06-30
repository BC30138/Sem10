#ifndef _MPIALG_H_
#define _MPIALG_H_
#include "../tools/TridiagonalSLE.h"
using namespace std;

class MPIalg : public TridiagonalSLE{
  public:
    MPIalg(): TridiagonalSLE() {}
    MPIalg(unsigned long len_of_middle):  TridiagonalSLE(len_of_middle) { }
    void solve(int thread_num);  
    ~MPIalg() {
      a.clear();
      b.clear();
      c.clear();
      d.clear();
      x.clear();
    }
};

#endif