#include<iostream>
#include<fstream>
#include <omp.h>
#include <vector>
#include <math.h>
#include"OpenMPalg.h"
#include"../tools/functions.h"
using namespace std;

void OpenMPalg::solve(int thread_num) {
    vector<double> a_temp(n);
    vector<double> d_temp(n);
    int k = floor(double(n) / double(thread_num));
    int last_thread_dif = n % k;

    vector<double> b_bound(thread_num - 1);
    vector<double> a_bound(thread_num);
    vector<double> c_bound(thread_num - 1);
    vector<double> d_bound(thread_num);
    vector<double> x_bound;
    x_bound.resize(thread_num);

    #pragma omp parallel num_threads(thread_num)
    {   
        int thread = omp_get_thread_num(); 
        int row_num;
        if (thread != thread_num - 1) row_num = k;
        else row_num = k + last_thread_dif;

        int row_start = thread * k;
        int row_end = row_start + row_num; 

        bool first_thread = false;
        bool last_thread = false;

        if (thread == 0) first_thread = true;
        else if (thread == thread_num - 1) last_thread = true;

        vector<double> b_thread; 
        vector<double> a_thread;
        vector<double> c_thread;
        vector<double> f_thread;
        vector<double> g_thread;
        vector<double> d_thread;
        vector<double> x_thread;

        x_thread.resize(row_num);

        if (first_thread) {
            b_thread = get_subvector(b, row_start, row_end - 1);
            b_thread.insert(b_thread.begin(), 0);
        }
        else {
            b_thread = get_subvector(b, row_start - 1, row_end - 1);
            f_thread.resize(row_num);
        }
        g_thread.resize(row_num);
        a_thread = get_subvector(a, row_start, row_end);
        d_thread = get_subvector(d, row_start, row_end);
        if (last_thread) {
            c_thread = get_subvector(c, row_start, row_end - 1);
        }
        else c_thread = get_subvector(c, row_start, row_end);

        double tmp; 
        if (!first_thread) f_thread[0] = b_thread[0];  
        for (int r_it = 1; r_it < row_num; r_it++) {
            tmp = b_thread[r_it] / a_thread[r_it - 1];
            a_thread[r_it] = a_thread[r_it] - c_thread[r_it - 1] * tmp;
            d_thread[r_it] = d_thread[r_it] - d_thread[r_it - 1] * tmp;
            if (!first_thread) f_thread[r_it] = - f_thread[r_it - 1] * tmp;
        }

        #pragma omp critical 
        {
            for (int r_it = 0; r_it < row_num; r_it++) {
                a_temp[row_start + r_it] = a_thread[r_it];
                d_temp[row_start + r_it] = d_thread[r_it];
            }
        }

        #pragma omp barrier

        g_thread[row_num - 1] = c_thread[row_num - 2];
        for (int r_it = row_num - 3; r_it >= 0; r_it --) {
            tmp = c_thread[r_it] / a_thread[r_it + 1];
            d_thread[r_it] = d_thread[r_it] - d_thread[r_it + 1] * tmp;
            g_thread[r_it + 1] = g_thread[r_it + 1] - g_thread[r_it + 2] * tmp;
            if (!first_thread) f_thread[r_it] = f_thread[r_it] - f_thread[r_it + 1] * tmp;
        }
        if(first_thread) g_thread.erase(g_thread.begin());
        else {
            #pragma omp critical
            tmp = c[row_start - 1] / a_thread[0];
            g_thread[0] = g_thread[0] - g_thread[1] * tmp;
            d_temp[row_start - 1] = d_temp[row_start - 1] - d_thread[0] * tmp;
            a_temp[row_start - 1] = a_temp[row_start - 1] - f_thread[0] * tmp; 
        }

        #pragma omp barrier
        if(!last_thread) {
            a_thread[row_num - 1] = a_temp[row_end - 1];
            d_thread[row_num - 1] = d_temp[row_end - 1];
        }

        if (thread_num == 1) {   
            x_bound[0] = d_thread[row_num - 1] / a_thread[row_num - 1];
        }
        else {
            #pragma omp critical
            if(first_thread) {
                a_bound[0] = a_thread[row_num - 1];
                d_bound[0] = d_thread[row_num - 1];
            }
            else {
                b_bound[thread - 1] = f_thread[row_num - 1];
                a_bound[thread] = a_thread[row_num - 1];
                c_bound[thread - 1] = g_thread[0];
                d_bound[thread] = d_thread[row_num - 1];
            }
            
            #pragma omp barrier
            #pragma omp single 
            {
                x_bound = ThomasAlg(b_bound, a_bound, c_bound, d_bound);
            }
        }
        
        x_thread[row_num - 1] = x_bound[thread];
        if (first_thread) {
            for (int it = 0; it < row_num - 1; it++) {
                x_thread[it] = (d_thread[it] - g_thread[it] * x_bound[0]) / a_thread[it];
            }
        }
        else {
            for (int it = 0; it < row_num - 1; it++) {
                x_thread[it] = (d_thread[it] - g_thread[it + 1] * x_bound[thread] - f_thread[it] * x_bound[thread - 1]) / a_thread[it];
            }
        }

        #pragma omp critical
        {
            for (int r_it = 0; r_it < row_num; r_it++) {
                x[row_start + r_it] = x_thread[r_it];
            }
        }
    }
}