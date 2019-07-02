#include<iostream>
#include<fstream>
#include <mpi.h>
#include <vector>
#include <math.h>
#include<ctime>
#include"MPIalg.h"
#include"functions.h"
using namespace std;

void MPIalg::solve(bool compare_test, ostream &out) {
    int thread;
    int thread_num;

    vector<double> a_temp(n);
    vector<double> d_temp(n);
    unsigned long long k;
    unsigned long long last_thread_dif;

    MPI_Init(NULL, NULL);

    MPI_Comm_rank(MPI_COMM_WORLD, &thread);
    MPI_Comm_size(MPI_COMM_WORLD, &thread_num);

    vector<double> b_bound(thread_num - 1);
    vector<double> a_bound(thread_num);
    vector<double> c_bound(thread_num - 1);
    vector<double> d_bound(thread_num);
    vector<double> x_bound;
    x_bound.resize(thread_num);

    clock_t start;
    if (thread == 0) {
        if (compare_test) {
            start = clock();
        }
        k = floor(double(n) / double(thread_num));
        last_thread_dif = n % k;
    }

    MPI_Bcast(&k, 1, MPI_UNSIGNED_LONG, 0, MPI_COMM_WORLD);
    MPI_Bcast(&last_thread_dif, 1, MPI_UNSIGNED_LONG, 0, MPI_COMM_WORLD);

    unsigned long long row_num;
    if (thread != thread_num - 1) row_num = k;
    else row_num = k + last_thread_dif;
    unsigned long long row_start = thread * k;
    unsigned long long  row_end = row_start + row_num;

    vector<int> row_nums(thread_num);
    MPI_Allgather(&row_num, 1, MPI_INT, &row_nums[0], 1, MPI_INT, MPI_COMM_WORLD);

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
    for (unsigned long long r_it = 1; r_it < row_num; r_it++) {
        tmp = b_thread[r_it] / a_thread[r_it - 1];
        a_thread[r_it] = a_thread[r_it] - c_thread[r_it - 1] * tmp;
        d_thread[r_it] = d_thread[r_it] - d_thread[r_it - 1] * tmp;
        if (!first_thread) f_thread[r_it] = - f_thread[r_it - 1] * tmp;
    }

    int displ[thread_num];
    if (thread == 0) {
        double sum = 0;
        for (int i = 0; i < thread_num; ++i) {
            displ[i] = sum;
            sum += row_nums[i];
        }
    }

    MPI_Gatherv(&d_thread[0], row_nums[thread], MPI_DOUBLE, &d_temp[0], &row_nums[0], &displ[0], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&a_thread[0], row_nums[thread], MPI_DOUBLE, &a_temp[0], &row_nums[0], &displ[0], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(a_temp.data(), a_temp.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(d_temp.data(), d_temp.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    g_thread[row_num - 1] = c_thread[row_num - 2];

    for (long long r_it = row_num - 3; r_it >= 0; r_it --) {
        tmp = c_thread[r_it] / a_thread[r_it + 1];
        d_thread[r_it] = d_thread[r_it] - d_thread[r_it + 1] * tmp;
        g_thread[r_it + 1] = g_thread[r_it + 1] - g_thread[r_it + 2] * tmp;
        if (!first_thread) f_thread[r_it] = f_thread[r_it] - f_thread[r_it + 1] * tmp;
    }

    if(first_thread) g_thread.erase(g_thread.begin());
    else {
        tmp = c[row_start - 1] / a_thread[0];
        g_thread[0] = g_thread[0] - g_thread[1] * tmp;
        d_temp[row_start - 1] = d_temp[row_start - 1] - d_thread[0] * tmp;
        a_temp[row_start - 1] = a_temp[row_start - 1] - f_thread[0] * tmp;
    }

    if (!last_thread) {
        a_temp.erase(a_temp.begin() + row_end - 1, a_temp.end());
        d_temp.erase(d_temp.begin() + row_end - 1, d_temp.end());
    }
    if (!first_thread) {
        a_temp.erase(a_temp.begin(), a_temp.begin() + row_start - 1);
        d_temp.erase(d_temp.begin(), d_temp.begin() + row_start - 1);
    }

    int size_ = a_temp.size();
    MPI_Allgather(&size_, 1, MPI_INT, &row_nums[0], 1, MPI_INT, MPI_COMM_WORLD);

    if (thread == 0) {
        double sum = 0;
        for (int i = 0; i < thread_num; ++i) {
            displ[i] = sum;
            sum += row_nums[i];
        }
    }

    vector<double> tmp_a(n);
    vector<double> tmp_d(n);
    MPI_Gatherv(&a_temp[0], row_nums[thread], MPI_DOUBLE, &tmp_a[0], &row_nums[0], &displ[0], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&d_temp[0], row_nums[thread], MPI_DOUBLE, &tmp_d[0], &row_nums[0], &displ[0], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    a_temp = tmp_a;
    d_temp = tmp_d;
    MPI_Bcast(a_temp.data(), a_temp.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(d_temp.data(), d_temp.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    tmp_a.clear();
    tmp_d.clear();

    if(!last_thread) {
        a_thread[row_num - 1] = a_temp[row_end - 1];
        d_thread[row_num - 1] = d_temp[row_end - 1];
    }

    if (thread_num == 1) {
        x_bound[0] = d_thread[row_num - 1] / a_thread[row_num - 1];
    }
    else {
        double b_bound_loc;
        double a_bound_loc;
        double c_bound_loc;
        double d_bound_loc;
        if(first_thread) {
            a_bound[0] = a_thread[row_num - 1];
            d_bound[0] = d_thread[row_num - 1];
            for (int it = 1; it < thread_num; it++) {
                MPI_Recv(&b_bound_loc, 1, MPI_DOUBLE, it, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Recv(&a_bound_loc, 1, MPI_DOUBLE, it, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Recv(&c_bound_loc, 1, MPI_DOUBLE, it, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Recv(&d_bound_loc, 1, MPI_DOUBLE, it, 3, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                b_bound[it - 1] = b_bound_loc;
                a_bound[it] = a_bound_loc;
                c_bound[it - 1] = c_bound_loc;
                d_bound[it] = d_bound_loc;
            }
        }
        else {
            b_bound_loc = f_thread[row_num - 1];
            a_bound_loc = a_thread[row_num - 1];
            c_bound_loc = g_thread[0];
            d_bound_loc = d_thread[row_num - 1];
            MPI_Send(&b_bound_loc, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
            MPI_Send(&a_bound_loc, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
            MPI_Send(&c_bound_loc, 1, MPI_DOUBLE, 0, 2, MPI_COMM_WORLD);
            MPI_Send(&d_bound_loc, 1, MPI_DOUBLE, 0, 3, MPI_COMM_WORLD);
        }

        if (first_thread) x_bound = ThomasAlg(b_bound, a_bound, c_bound, d_bound);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Bcast(x_bound.data(), x_bound.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    x_thread[row_num - 1] = x_bound[thread];
    if (first_thread) {
        for (unsigned long long it = 0; it < row_num - 1; it++) {
            x_thread[it] = (d_thread[it] - g_thread[it] * x_bound[0]) / a_thread[it];
        }
    }
    else {
        for (unsigned long long it = 0; it < row_num - 1; it++) {
            x_thread[it] = (d_thread[it] - g_thread[it + 1] * x_bound[thread] - f_thread[it] * x_bound[thread - 1]) / a_thread[it];
        }
    }

    MPI_Allgather(&row_num, 1, MPI_INT, &row_nums[0], 1, MPI_INT, MPI_COMM_WORLD);

    if (thread == 0) {
        double sum = 0;
        for (int i = 0; i < thread_num; ++i) {
            displ[i] = sum;
            sum += row_nums[i];
        }
    }

    MPI_Gatherv(&x_thread[0], row_nums[thread], MPI_DOUBLE, &x[0], &row_nums[0], &displ[0], MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(x.data(), x.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    MPI_Finalize();

    if (thread == 0) {
        if (compare_test) {
            out << thread_num << "\t" << (clock() - start) / (double)CLOCKS_PER_SEC << endl;
        }
        else show_result();
    }

}