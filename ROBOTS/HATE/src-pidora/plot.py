import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib import cm
import pylab
import numpy as np

def show_map(matrix, pathes):
    cax = plt.matshow(matrix, cmap=cm.terrain)
    plt.colorbar()
    plt.clim(0, 1)
    for path in pathes:
        coordinate_x = [path[0][1], path[-1][1]]
        coordinate_y = [path[0][0], path[-1][0]]
        order_x = [i[1] for i in path]
        order_y = [i[0] for i in path]
        plt.plot(coordinate_x[0], coordinate_y[0], 'ro',coordinate_x[1], coordinate_y[1], 'bo', order_x, order_y, 'k')
    plt.pause(0.05)
    plt.show()

def show_heuristic(matrix, tau):
    cax = plt.matshow(matrix, cmap=cm.terrain)
    plt.colorbar()
    plt.clim(0, tau)

    plt.pause(0.05)
    plt.show()