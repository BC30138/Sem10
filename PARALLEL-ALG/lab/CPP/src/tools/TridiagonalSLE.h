#ifndef _TRIDIAGONALSLE_H_
#define _TRIDIAGONALSLE_H_
#include<vector>
#include<iostream>
using namespace std;

class TridiagonalSLE {
  protected:  
    vector<double> b;
    vector<double> a;
    vector<double> c;
    vector<double> d;
    vector<double> x;
    unsigned long n;
    void export_to(ostream& output_stream);

  public:
    TridiagonalSLE();
    TridiagonalSLE(int len_of_middle);
    void generate_random_SLE(unsigned long len_of_middle);
    void solve();
    void show();
    void show_result();
    unsigned long size();
    vector<double> get_result();
    void export_data(string file_path);
    void read_data(string file_path);
};

#endif