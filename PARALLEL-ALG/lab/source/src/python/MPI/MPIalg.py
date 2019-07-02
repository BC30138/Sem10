from mpi4py import MPI
import numpy as np
import math
from time import time

def ThomasAlg(b, a, c, d):
    n = np.int64(len(d))
    alpha = np.empty(n - 1)
    beta = np.empty(n - 1)
    x = np.empty(n)

    alpha[0] = - c[0] / a[0];
    beta[0] = d[0] / a[0];

    for it in range(1, n - 1):
        y = a[it] + b[it - 1] * alpha[it - 1]
        alpha[it] = - c[it] / y
        beta[it] = (d[it] - b[it - 1] * beta[it - 1]) / y

    x[n - 1] = (d[n - 1] - b[n - 2] * beta[n - 2]) / (a[n - 1] + b[n - 2] * alpha[n - 2])

    for it in reversed(range(n - 1)):
        x[it] = alpha[it] * x[it + 1] + beta[it]
    return x

class MPIalg:
    def __init__(self, **kwargs):
        if kwargs:
            lower_bound = 0;
            upper_bound = 10;
            self.n = kwargs["n"];
            self.b = np.zeros(self.n - 1);
            self.a = np.zeros(self.n);
            self.c = np.zeros(self.n - 1);
            self.d = np.zeros(self.n);
            self.x = np.zeros(self.n);

            np.random.seed(3)
            self.a[0] = np.random.uniform(low=lower_bound, high=upper_bound)
            self.d[0] = np.random.uniform(low=lower_bound, high=upper_bound)

            for it in range(self.n - 1):
                self.b[it] = np.random.uniform(low=lower_bound, high=upper_bound)
                self.c[it] = np.random.uniform(low=lower_bound, high=upper_bound)
                self.a[it + 1] = np.random.uniform(low=lower_bound, high=upper_bound)
                self.d[it + 1] = np.random.uniform(low=lower_bound, high=upper_bound)

        else:
            self.b = np.array(0)
            self.a = np.array(0)
            self.c = np.array(0)
            self.d = np.array(0)
            self.x = np.array(0)
            self.n = np.int64(0)

    def read_data(self, file_path):
        f=open(file_path, "r")
        s_tmp = list(map(str.strip, f.readlines()))
        self.n = np.int64(s_tmp[0].split()[1])

        """b read"""
        self.b = s_tmp[1].replace('\t',' ').split()
        del self.b[0]
        self.b = list(map(float, self.b))

        """a read"""
        self.a = s_tmp[2].replace('\t',' ').split()
        del self.a[0]
        self.a = list(map(float, self.a))

        """c read"""
        self.c = s_tmp[3].replace('\t',' ').split()
        del self.c[0]
        self.c = list(map(float, self.c))

        """d read"""
        self.d = s_tmp[14].replace('\t',' ').split()
        del self.d[0]
        self.d = list(map(float, self.d))

        self.x = np.zeros(self.n)

    def solve(self, **kwargs):
        comm = MPI.COMM_WORLD
        thread_num = comm.Get_size()
        thread = comm.Get_rank()

        a_temp = np.zeros(self.n)
        d_temp = np.zeros(self.n)

        b_bound = np.zeros(thread_num - 1)
        a_bound = np.zeros(thread_num)
        c_bound = np.zeros(thread_num - 1)
        d_bound = np.zeros(thread_num)
        x_bound = np.zeros(thread_num)

        if (thread == 0):
            if kwargs:
                start = time()
            k = np.int64(math.floor(float(self.n) / float(thread_num)))
            last_thread_dif = self.n % k
        else:
            k = np.int64(0)
            last_thread_dif = np.int64(0)

        k = comm.bcast(k, 0)

        if (thread != thread_num - 1): row_num = k;
        else: row_num = k + last_thread_dif;
        row_start = thread * k;
        row_end = row_start + row_num;

        row_nums = np.zeros(thread_num, dtype=np.int64);
        comm.Allgather([row_num, MPI.LONG],[row_nums, MPI.LONG])

        first_thread = False
        last_thread = False

        if (thread == 0): first_thread = True
        else:
            if (thread == thread_num - 1): last_thread = True

        if first_thread:
            b_thread = np.zeros(1)
            b_thread = np.concatenate((b_thread, self.b[row_start:row_end - 1]))
        else:
            b_thread = np.array(self.b[row_start - 1:row_end - 1])
            f_thread = np.zeros(row_num)
        g_thread = np.zeros(row_num)
        a_thread = np.array(self.a[row_start:row_end])
        d_thread = np.array(self.d[row_start:row_end])
        if last_thread:
            c_thread = np.array(self.c[row_start:row_end - 1])
        else: c_thread = np.array(self.c[row_start:row_end])
        x_thread = np.empty(row_num)

        if not first_thread: f_thread[0] = b_thread[0]
        for r_it in range(1, row_num):
            tmp = b_thread[r_it] / a_thread[r_it - 1];
            a_thread[r_it] = a_thread[r_it] - c_thread[r_it - 1] * tmp
            d_thread[r_it] = d_thread[r_it] - d_thread[r_it - 1] * tmp
            if not first_thread: f_thread[r_it] = - f_thread[r_it - 1] * tmp

        comm.Gatherv(sendbuf=a_thread, recvbuf=(a_temp, row_nums), root=0)
        comm.Gatherv(sendbuf=d_thread, recvbuf=(d_temp, row_nums), root=0)
        a_temp = comm.bcast(a_temp, 0)
        d_temp = comm.bcast(d_temp, 0)

        g_thread[row_num - 1] = c_thread[row_num - 2]

        for r_it in reversed(range(0, row_num - 2)):
            tmp = c_thread[r_it] / a_thread[r_it + 1]
            d_thread[r_it] = d_thread[r_it] - d_thread[r_it + 1] * tmp
            g_thread[r_it + 1] = g_thread[r_it + 1] - g_thread[r_it + 2] * tmp
            if not first_thread: f_thread[r_it] = f_thread[r_it] - f_thread[r_it + 1] * tmp

        if first_thread: g_thread = np.delete(g_thread, 0)
        else :
            tmp = self.c[row_start - 1] / a_thread[0]
            g_thread[0] = g_thread[0] - g_thread[1] * tmp
            d_temp[row_start - 1] = d_temp[row_start - 1] - d_thread[0] * tmp
            a_temp[row_start - 1] = a_temp[row_start - 1] - f_thread[0] * tmp

        if not last_thread:
            a_temp = np.delete(a_temp, np.s_[row_end - 1:self.n])
            d_temp = np.delete(d_temp, np.s_[row_end - 1:self.n])
        if not first_thread:
            a_temp = np.delete(a_temp, np.s_[0:row_start - 1])
            d_temp = np.delete(d_temp, np.s_[0:row_start - 1])

        size_ = np.int64(len(a_temp))
        comm.Allgather([size_, MPI.LONG],[row_nums, MPI.LONG])

        tmp_a = np.empty(self.n)
        tmp_d = np.empty(self.n)
        comm.Gatherv(sendbuf=a_temp, recvbuf=(tmp_a, row_nums), root=0)
        comm.Gatherv(sendbuf=d_temp, recvbuf=(tmp_d, row_nums), root=0)
        a_temp = tmp_a
        d_temp = tmp_d
        a_temp = comm.bcast(a_temp, 0)
        d_temp = comm.bcast(d_temp, 0)
        del tmp_a
        del tmp_d

        if not last_thread:
            a_thread[row_num - 1] = a_temp[row_end - 1]
            d_thread[row_num - 1] = d_temp[row_end - 1]

        if (thread_num == 1):
            x_bound[0] = d_thread[row_num - 1] / a_thread[row_num - 1]
        else :
            if first_thread:
                a_bound[0] = a_thread[row_num - 1]
                d_bound[0] = d_thread[row_num - 1]
                for it in range(1, thread_num):
                    b_bound[it - 1] = comm.recv(source=it, tag=0)
                    a_bound[it] = comm.recv(source=it, tag=1)
                    c_bound[it - 1] = comm.recv(source=it, tag=2)
                    d_bound[it] = comm.recv(source=it, tag=3)
            else :
                comm.send(f_thread[row_num - 1], dest=0, tag=0)
                comm.send(a_thread[row_num - 1], dest=0, tag=1)
                comm.send(g_thread[0], dest=0, tag=2)
                comm.send(d_thread[row_num - 1], dest=0, tag=3)
            if first_thread: x_bound = ThomasAlg(b_bound, a_bound, c_bound, d_bound);

        comm.barrier()
        x_bound = comm.bcast(x_bound, 0)

        x_thread[row_num - 1] = x_bound[thread];
        if first_thread:
            for it in range(row_num - 1): x_thread[it] = (d_thread[it] - g_thread[it] * x_bound[0]) / a_thread[it]
        else:
            for it in range(row_num - 1):
                x_thread[it] = (d_thread[it] - g_thread[it + 1] * x_bound[thread] - f_thread[it] * x_bound[thread - 1]) / a_thread[it]

        comm.Allgather([row_num, MPI.LONG],[row_nums, MPI.LONG])
        comm.Gatherv(sendbuf=x_thread, recvbuf=(self.x, row_nums), root=0)

        if (thread == 0):
            if kwargs:
                f = open(kwargs["filepath"], "a")
                f.write(str(thread_num) + "\t" + str(time() - start) + "\n")
            else: print(self.x)
