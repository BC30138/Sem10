"""usefull functions"""
import math
import bisect
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D

def generate_tables(sizes, targets_numbers):
    for it, _ in enumerate(sizes):
        matrix_ant = np.zeros((11, len(targets_numbers)))
        matrix_plan = np.zeros((11, len(targets_numbers)))
        matrix_full = np.zeros((11, len(targets_numbers)))
        caption = str(sizes[it]) + "x" + str(sizes[it])
        root = "data/time/" + caption + "/"
        for jt, _ in enumerate(targets_numbers):
            file_path = root + str(targets_numbers[jt]) + ".data"
            file = open(file_path)
            lines = file.readlines()
            for kt in range(3,13):
                matrix_ant[kt - 3][jt] = float(lines[kt].rstrip().rsplit("\t")[1])
                matrix_plan[kt - 3][jt] = float(lines[kt].rstrip().rsplit("\t")[2])
                matrix_full[kt - 3][jt] = float(lines[kt].rstrip().rsplit("\t")[3])
            matrix_ant[10][jt] = float(lines[13].rstrip().rsplit("\t")[1])
            matrix_plan[10][jt] = float(lines[14].rstrip().rsplit("\t")[2])
            matrix_full[10][jt] = float(lines[15].rstrip().rsplit("\t")[3])
        print_tex_table(matrix_ant, targets_numbers, "data/tex_tables/ant_time/" + caption + ".tex", "Размер карты: " + caption)
        print_tex_table(matrix_plan, targets_numbers, "data/tex_tables/plan_time/" + caption + ".tex", "Размер карты: " + caption)
        print_tex_table(matrix_full, targets_numbers, "data/tex_tables/full_time/" + caption + ".tex", "Размер карты: " + caption)

def print_tex_table(matrix, targets_numbers, file_name, caption):
    """print latex formated table from matrix"""
    file = open(file_name, "w+")
    file.write("\\begin{table}[H]\n")
    file.write("\\centering\n")
    file.write("\\begin{tabular}{|r|l|l|l|l|}\n")
    file.write("\\hline\n")
    line = "№ карты\\textbackslash Кол-во роботов"
    for num in targets_numbers:
        line += " & \\textbf{" + str(num) + "}"
    line += "\\\\ \\hline\n"
    file.write(line)
    for it in range(matrix.shape[0] - 1):
        line = str(it + 1)
        for jt in range(matrix.shape[1]):
            line += " & " + str(round(matrix[it][jt], 5))
        line += "\\\\ \\hline\n"
        file.write(line)
    line = "Средний элемент"
    for jt in range(matrix.shape[1]):
        line += " & " + str(round(matrix[10][jt], 5))
    line += "\\\\ \\hline\n"
    file.write(line)
    file.write("\\end{tabular}\n")
    file.write("\\caption*{" + caption + "}\n")
    file.write("\\end{table}\n")

def plot_surface(matrix, sizes, targets_numbers, file_name):
    """Plot 3d surface"""
    rcParams.update({'font.size': 16})
    (x, y) = np.meshgrid(np.arange(matrix.shape[1]), np.arange(matrix.shape[0]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, np.log(matrix), cmap=plt.get_cmap("viridis"))
    ax.set_xlabel('Targets', labelpad=20)
    ax.set_ylabel('Map size', labelpad=20)
    ax.set_zlabel('ln(t)', labelpad=10)
    plt.xticks(range(len(targets_numbers)), targets_numbers)
    plt.yticks(range(len(sizes)), sizes)
    fig.colorbar(surf)
    fig.set_size_inches(12.5, 8.5)
    fig.savefig(file_name, dpi=100)
    plt.close(fig)

def plot_time_correlation(sizes, targets_numbers):
    """tool for plot surface from time data"""
    matrix = np.zeros((len(sizes), len(targets_numbers)))
    for it, _ in enumerate(sizes):
        root = "data/time/" + str(sizes[it]) + "x" + str(sizes[it]) + "/"
        for jt, _ in enumerate(targets_numbers):
            file_path = root + str(targets_numbers[jt]) + ".data"
            file = open(file_path)
            mean_time = float(file.readlines()[15].rstrip().rsplit("\t")[3])
            matrix[it][jt] = round(mean_time, 3)
    plot_surface(matrix, sizes, targets_numbers, "data/time/mean_surface.png")

def plot_map(graph, file_name):
    """Plot map in heatmap format"""
    plot_heatmap(graph.get_matrix(), file_name)

def plot_paths(graph, paths, file_name):
    """Plot paths on map"""
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
    plt.close(fig)

def plot_path(graph, path, file_name):
    """Plot single path on map"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pl = ax.imshow(graph.get_matrix(), cmap=plt.get_cmap("gist_earth"))
    fig.colorbar(pl)
    fig.set_size_inches(8.5, 8.5)
    ax.plot([x for x, y in path], [y for x, y in path], linewidth=2.0, c="orange")
    ax.plot(path[0][0], path[0][1], "ro", c="black")
    ax.plot(path[len(path) - 1][0], path[len(path) - 1][1], "ro", c="red")
    fig.savefig(file_name, dpi=100)
    plt.close(fig)

def plot_heuristic_d(graph, file_name):
    """Plot heuristic by distance in heatmap format"""
    plot_heatmap(graph.heuristic_d, file_name)

def plot_pheromone(graph, file_name):
    """Plot pheromone heatmap"""
    plot_heatmap(graph.pheromone, file_name)

def plot_heatmap(matrix, file_name):
    """Plot 2d heat map"""
    fig = plt.figure()
    ax = plt.imshow(np.transpose(matrix), cmap=plt.get_cmap("gist_earth"))
    fig.colorbar(ax)
    fig.set_size_inches(8.5, 8.5)
    fig.savefig(file_name, dpi=100)
    plt.close(fig)

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