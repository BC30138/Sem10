#ifndef _FUNCTIONS_H_
#define _FUNCTIONS_H_
#include<vector>
#include<iostream>
using namespace std;

void print_vector(vector<double> vec, ostream& out);
vector<double> string_to_d_vector(string str);
vector<double> get_subvector(vector<double> vec, int begin, int end);
vector<double> ThomasAlg(vector<double> b, vector<double> a, vector<double> c, vector<double> d);

#endif