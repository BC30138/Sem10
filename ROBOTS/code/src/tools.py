"""usefull functions"""
import random
import bisect
import collections
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_path(matrix, way, save_path):
    """plor 3d surface"""
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    z = list()
    for it in range(len(x)):
        list.append(path_z, matrix[path_x[it]][path_y[it]])
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.set_size_inches(20.5, 8.5)
    path_x = [x[0] for x in way]
    path_y = [x[1] for x in way]
    path_z = list()
    for it in range(len(way)):
        list.append(path_z, matrix[path_x[it]][path_y[it]])
    ax.plot(path_x, path_y, path_z, 'ro')
    surf = ax.plot_surface(x, y, matrix, rstride=1, cstride=1, cmap=plt.get_cmap("viridis"), edgecolor='none')
    fig.colorbar(surf)
    plt.show()
    # fig.savefig(save_path, dpi=100)

def surface_plot(matrix, path):
    """plor 3d surface"""
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, matrix, cmap=plt.get_cmap("viridis"))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.colorbar(surf)
    fig.set_size_inches(20.5, 8.5)
    fig.savefig(path, dpi=100)

def cdf(weights):
    """generate weights"""
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    """choice with prob"""
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]
