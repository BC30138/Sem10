import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D

def plot_line(x, y, x_label, y_label, file_path, label):
    """plot line"""
    rcParams.update({'font.size': 16})
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, '-ro', linewidth=2.0, label=label)
    ax.set_xlabel(x_label, labelpad=20)
    ax.set_ylabel(y_label, labelpad=20)
    ax.legend(loc='best')
    plt.xticks(range(1, len(x) + 1), list(map(int, x)))
    fig.set_size_inches(12.5, 8.5)
    fig.savefig(file_path, dpi=100)
    plt.close(fig)

def read(file_name):
    f = open(file_name, "r")
    file_lines = list(map(str.strip, f.readlines()))
    x = np.empty(0)
    y = np.empty(0)
    for it in range(2, len(file_lines)):
        norm_line = file_lines[it].split("\t")
        x = np.append(x, int(norm_line[0]))
        y = np.append(y, float(norm_line[1]))
    return x, y

x, y = read("run1/MPIPythonTime.data")
plot_line(x, y, "number of processes (threads)", "time (s.)", "plots/MPIPython.png", "MPI Python")
x, y = read("run1/MPITime.data")
plot_line(x, y, "number of processes (threads)", "time (s.)", "plots/MPI.png", "MPI C++")
x, y = read("run1/OMPtime.data")
plot_line(x, y, "number of processes (threads)", "time (s.)", "plots/OMP.png", "OpenMP")
x, y = read("run1/Pthreadstime.data")
plot_line(x, y, "number of processes (threads)", "time (s.)", "plots/pthreads.png", "pthreads")
