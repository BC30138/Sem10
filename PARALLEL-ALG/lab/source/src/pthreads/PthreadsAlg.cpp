#include<iostream>
#include<fstream>
#include <vector>
#include <math.h>
#include <pthread.h>
#include"PthreadsAlg.h"
#include"../tools/functions.h"
using namespace std;

unsigned long long k;
unsigned long long last_thread_dif;
int thread_num;

vector<double> a_temp;
vector<double> d_temp;

vector<double> b_bound;
vector<double> a_bound;
vector<double> c_bound;
vector<double> d_bound;
vector<double> x_bound;

vector<double> *b_global;
vector<double> *a_global;
vector<double> *c_global;
vector<double> *d_global;
vector<double> *x_global;

pthread_mutex_t mutex_1;
static pthread_barrier_t barrier;
pthread_mutex_t mutex_2;
pthread_mutex_t mutex_3;
pthread_mutex_t mutex_4;

void *thread_func(void *thread_id) {
    // struct arg_struct *args = (struct arg_struct *)arguments;

    int thread = *((int*)(&thread_id));

    unsigned long long row_num;
    if (thread != thread_num - 1) row_num = k;
    else row_num = k + last_thread_dif;

    unsigned long long row_start = thread * k;
    unsigned long long  row_end = row_start + row_num;

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
        b_thread = get_subvector(*b_global, row_start, row_end - 1);
        b_thread.insert(b_thread.begin(), 0);
    }
    else {
        b_thread = get_subvector(*b_global, row_start - 1, row_end - 1);
        f_thread.resize(row_num);
    }
    g_thread.resize(row_num);
    a_thread = get_subvector(*a_global, row_start, row_end);
    d_thread = get_subvector(*d_global, row_start, row_end);
    if (last_thread) {
        c_thread = get_subvector(*c_global, row_start, row_end - 1);
    }
    else c_thread = get_subvector(*c_global, row_start, row_end);

    double tmp;
    if (!first_thread) f_thread[0] = b_thread[0];
    for (unsigned long long r_it = 1; r_it < row_num; r_it++) {
        tmp = b_thread[r_it] / a_thread[r_it - 1];
        a_thread[r_it] = a_thread[r_it] - c_thread[r_it - 1] * tmp;
        d_thread[r_it] = d_thread[r_it] - d_thread[r_it - 1] * tmp;
        if (!first_thread) f_thread[r_it] = - f_thread[r_it - 1] * tmp;
    }

    pthread_mutex_lock(&mutex_1);
        for (unsigned long long r_it = 0; r_it < row_num; r_it++) {
            a_temp[row_start + r_it] = a_thread[r_it];
            d_temp[row_start + r_it] = d_thread[r_it];
        }
    pthread_mutex_unlock(&mutex_1);

    pthread_barrier_wait(&barrier);

    g_thread[row_num - 1] = c_thread[row_num - 2];
    for (long long r_it = row_num - 3; r_it >= 0; r_it --) {
        tmp = c_thread[r_it] / a_thread[r_it + 1];
        d_thread[r_it] = d_thread[r_it] - d_thread[r_it + 1] * tmp;
        g_thread[r_it + 1] = g_thread[r_it + 1] - g_thread[r_it + 2] * tmp;
        if (!first_thread) f_thread[r_it] = f_thread[r_it] - f_thread[r_it + 1] * tmp;
    }
    if(first_thread) g_thread.erase(g_thread.begin());
    else {
        pthread_mutex_lock(&mutex_2);
            tmp = c_global[0][row_start - 1] / a_thread[0];
            g_thread[0] = g_thread[0] - g_thread[1] * tmp;
            d_temp[row_start - 1] = d_temp[row_start - 1] - d_thread[0] * tmp;
            a_temp[row_start - 1] = a_temp[row_start - 1] - f_thread[0] * tmp;
        pthread_mutex_unlock(&mutex_2);
    }

    pthread_barrier_wait(&barrier);

    if(!last_thread) {
        a_thread[row_num - 1] = a_temp[row_end - 1];
        d_thread[row_num - 1] = d_temp[row_end - 1];
    }

    if (thread_num == 1) {
        x_bound[0] = d_thread[row_num - 1] / a_thread[row_num - 1];
    }
    else {
        pthread_mutex_lock(&mutex_3);
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
        pthread_mutex_unlock(&mutex_3);

        pthread_barrier_wait(&barrier);

        if (thread == 0) {
            x_bound = ThomasAlg(b_bound, a_bound, c_bound, d_bound);
        }

        pthread_barrier_wait(&barrier);
    }

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

    pthread_mutex_lock(&mutex_4);
    for (unsigned long long r_it = 0; r_it < row_num; r_it++) {
        x_global[0][row_start + r_it] = x_thread[r_it];
    }
    pthread_mutex_unlock(&mutex_4);

    pthread_exit(NULL);

    return NULL;
}

void PthreadsAlg::solve(int t_num) {
    thread_num = t_num;
    pthread_t threads[thread_num];

    b_global = &b;
    a_global = &a;
    c_global = &c;
    d_global = &d;
    x_global = &x;

    a_temp.resize(n);
    d_temp.resize(n);
    k = floor(double(n) / double(thread_num));
    last_thread_dif = n % k;

    b_bound.resize(thread_num - 1);
    a_bound.resize(thread_num);
    c_bound.resize(thread_num - 1);
    d_bound.resize(thread_num);
    x_bound.resize(thread_num);

    pthread_mutex_init(&mutex_1, NULL);
    pthread_barrier_init(&barrier, NULL, thread_num);
    pthread_mutex_init(&mutex_2, NULL);
    pthread_mutex_init(&mutex_3, NULL);
    pthread_mutex_init(&mutex_4, NULL);
    for (int it = 0; it < thread_num; it++) {
        pthread_create(&threads[it], NULL, thread_func, (void *) it);
    }
    for (int it = 0; it < thread_num; it++) {
        pthread_join(threads[it], NULL);
    }

    pthread_mutex_destroy(&mutex_1);
    pthread_barrier_destroy(&barrier);
    pthread_mutex_destroy(&mutex_2);
    pthread_mutex_destroy(&mutex_3);
    pthread_mutex_destroy(&mutex_4);
}