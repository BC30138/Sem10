import math
import bisect
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_surface(graph, file_name):
    """Plot 3d surface"""
    (x, y) = np.meshgrid(np.arange(graph.get_size()[0]), np.arange(graph.get_size()[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, graph.get_matrix(), cmap=plt.get_cmap("gist_earth"))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.colorbar(surf)
    fig.set_size_inches(20.5, 8.5)
    plt.show()

def plot_map(graph, file_name):
    """Plot map in heatmap format"""
    plot_heatmap(graph.get_matrix(), file_name)

def plot_paths(graph, paths, file_name):
    """Plot path on map"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pl = ax.imshow(graph.get_matrix(), cmap=plt.get_cmap("gist_earth"))
    fig.colorbar(pl)
    fig.set_size_inches(8.5, 8.5)
    for path in paths:
        ax.plot([x for x, y in path], [y for x, y in path], linewidth=2.0, c="orange")
        ax.plot(path[0][0], path[0][1], "ro", c="black")
        ax.plot(path[len(path) - 1][0], path[len(path) - 1][1], "ro", c="red")
    fig.savefig(file_name, dpi=100)

def plot_heuristic_d(graph, file_name):
    """Plot heuristic by distance in heatmap format"""
    plot_heatmap(graph.heuristic_d, file_name)

def plot_pheromone(graph, file_name):
    """Plot pheromone heatmap"""
    plot_heatmap(graph.pheromone, file_name)

def plot_heatmap(matrix, file_name):
    """Plot 2d heat map"""
    fig = plt.figure()
    ax = plt.imshow(matrix, cmap=plt.get_cmap("gist_earth"))
    fig.colorbar(ax)
    fig.set_size_inches(8.5, 8.5)
    fig.savefig(file_name, dpi=100)

def cdf(weights):
    """generate weights"""
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(weights):
    """choice with prob"""
    cdf_vals = cdf(weights)
    x = np.random.uniform(low=0.0, high=1.0)
    idx = bisect.bisect(cdf_vals, x)
    return idx

def get_conj(matrix, point):
    """returns conjugate points for point in matrix"""
    conj_points = []
    top_left = True
    top_right = True
    bottom_left = True
    bottom_right = True
    if point[0] > 0:
        conj_points.append([point[0] - 1, point[1]])
    else:
        top_left = False
        top_right = False
    if point[0] < matrix.shape[0] - 1:
        conj_points.append([point[0] + 1, point[1]])
    else:
        bottom_left = False
        bottom_right = False
    if point[1] > 0:
        conj_points.append([point[0], point[1] - 1])
    else:
        bottom_left = False
        top_left = False
    if point[1] < matrix.shape[1] - 1:
        conj_points.append([point[0], point[1] + 1])
    else:
        top_right = False
        bottom_right = False

    if top_left:
        conj_points.append([point[0] - 1, point[1] - 1])
    if top_right:
        conj_points.append([point[0] - 1, point[1] + 1])
    if bottom_left:
        conj_points.append([point[0] + 1, point[1] - 1])
    if bottom_right:
        conj_points.append([point[0] + 1, point[1] + 1])

    return conj_points

def get_distance_proj(x, y):
    """distance between two point by x and y using Euclid metric"""
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def get_distance(x, y, matrix):
    """distance between two point by x, y and z using Euclid metric"""
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (matrix[x[0]][x[1]] - matrix[y[0]][y[1]]) ** 2)

def get_mean(some_list):
    """Returns mean value of list"""
    return sum(some_list) / len(some_list)

def to_vector(input_map):
    vec = []
    for i in range(len(input_map)):
        for j in range(len(input_map)):
            vec.append(input_map[i][j])
    return vec
