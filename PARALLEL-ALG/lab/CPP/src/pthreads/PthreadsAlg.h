#ifndef _PTHREADS_H_
#define _PTHREADS_H_
#include "../tools/TridiagonalSLE.h"
using namespace std;

class PthreadsAlg : public TridiagonalSLE{
  public:
    PthreadsAlg(): TridiagonalSLE() {}
    PthreadsAlg(unsigned long len_of_middle):  TridiagonalSLE(len_of_middle) { }
    void solve(int thread_num);  
    ~PthreadsAlg() {
      a.clear();
      b.clear();
      c.clear();
      d.clear();
      x.clear();
    }
};

#endif