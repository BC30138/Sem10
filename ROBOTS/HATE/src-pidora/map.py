import plot as pl
import aco
import numpy as np
import time

import DiamondSquare as ds

size = 50
tau = 1
robots_number = 5

sign = lambda x: (1, -1)[x<0]

def calc_effective(robot, target):
    rb_xy = aco.get_vert_by_code(robot, size)
    tg_xy = aco.get_vert_by_code(target, size)
    return abs(rb_xy[0] - tg_xy[0]) + abs(rb_xy[1] - tg_xy[1])

def kern(i, final, size):
    return ((final[0] - i[0]) ** 2 + (final[1] - i[1]) ** 2) / (2 * size ** 2)
    # return (abs (2 ** final[0] - 2 ** i[0]) + abs(2 ** final[1] - 2 ** i[1])) / (2 ** (size + 1))

def distance(h_i, h_j):
    return abs(h_i - h_j)

def pher_distance(ph_i, ph_j):
    return ph_i + ph_j


def create_pheromone(size, start, final):
    map_heuristic = np.zeros((size, size))
    start_coord = aco.get_vert_by_code(start, size)
    final_coord = aco.get_vert_by_code(final, size)
    # i = start_coord[0]
    # j = start_coord[1]
    # delta_x = sign(final_coord[0] - i)
    # delta_y = sign(final_coord[1] - j)
    # while abs(final_coord[0] - i) != 0 and abs(final_coord[1] - j) != 0:
    #     map_heuristic[i][j] = tau
    #     i += delta_x
    #     map_heuristic[i][j] = tau
    #     j += delta_y
    # while abs(final_coord[0] - i) != 0:
    #     map_heuristic[i][j] = tau
    #     i += delta_x
    # while abs(final_coord[1] - j) != 0:
    #     map_heuristic[i][j] = tau
    #     j += delta_y
    map_heuristic[final_coord[0]][final_coord[1]] = 2 * tau
    for x in range(len(map_heuristic)):
        for y in range(len(map_heuristic)):
            map_heuristic[x][y] += tau * (1 - kern([x,y], final_coord, size))
            # print(map_heuristic[x][y])
    return map_heuristic


def create_heuristic(size, final):
    map_heuristic = np.zeros((size, size))
    final_coord = aco.get_vert_by_code(final, size)
    absolute = 2 * (size - 1)
    map_heuristic[final_coord[0]][final_coord[1]] = absolute
    for x in range(len(map_heuristic)):
        for y in range(len(map_heuristic)):
            map_heuristic[x][y] = absolute - (abs(final_coord[0] - x) + abs(final_coord[1] - y))
    return map_heuristic


def get_cost_matrix(map):
    cost = []
    for i in range(len(map) - 1):
        for j in range(len(map) - 1):
            # fst = aco.get_code_by_vert[i][j]
            # snd = aco.get_code_by_vert[i][j + 1]
            # costn = aco.get_edge_number(fst, snd, size)
            cost.append(distance(map[i][j], map[i][j + 1]))
        for j in range(len(map)):
            cost.append(distance(map[i][j], map[i + 1][j]))
    for j in range(len(map) - 1):
        cost.append(distance(map[len(map) - 1][j], map[len(map) - 1][j + 1]))
    return cost


def get_pher_matrix(map):
    pher = []
    for i in range(len(map) - 1):
        for j in range(len(map) - 1):
            pher.append(pher_distance(map[i][j], map[i][j + 1]))
        for j in range(len(map)):
            pher.append(pher_distance(map[i][j], map[i + 1][j]))
    for j in range(len(map) - 1):
        pher.append(pher_distance(map[len(map) - 1][j], map[len(map) - 1][j + 1]))
    return pher


alpha = 1
beta = 1
evaporation = 0.9
q = 50
antNumber = 50
modification = 3
limit = 10

# map = ds.create_map(size)
# np.save(str(size) + '.txt', map)
map = np.load(str(size) + '.txt.npy')
map_vector = aco.enumerate_map(map)
xy_pathes = []

times = []
for a in range(9):
    starts = []
    finals = []


    for i in range(robots_number):
        starts.append(np.random.randint(0, size ** 2))
        finals.append(np.random.randint(0, size ** 2))
        while starts.count(starts[-1]) > 1 or finals.count(starts[-1]) > 0:
            starts.pop()
            starts.append(np.random.randint(0, size ** 2))
        while finals.count(finals[-1]) > 1 or starts.count(finals[-1]) > 0:
            finals.pop()
            finals.append(np.random.randint(0, size ** 2))

    # print(starts, finals)

    pairs = []
    effective = []

    for robot in starts:
        eff = []
        for target in finals:
            eff.append(calc_effective(robot, target))
        effective.append(eff)

    while len(pairs) < robots_number:
        minimum = float('inf')
        arg_min = 0
        arg_fin = 0
        for i in range(len(effective)):
            if min(effective[i]) < minimum:
                minimum = min(effective[i])
                arg_min = i
                arg_fin = np.argmin(effective[i])
        pairs.append([starts[arg_min], finals[arg_fin]])
        starts.pop(arg_min)
        finals.pop(arg_fin)
        effective.pop(arg_min)
        for row in effective:
            row.pop(arg_fin)


    startTime = time.time()
    for robot in pairs:
        start = robot[0]
        final = robot[1]
        pheromone_map = create_pheromone(size, start, final)
        heuristic_map = create_heuristic(size, final)
        pheromone_vector = aco.enumerate_map(pheromone_map)
        heuristic_vector = aco.enumerate_map(heuristic_map)
        cost_matrix = get_cost_matrix(map)
        # heuristic_matrix = get_pher_matrix(heuristic_map)
        # print(len(map_vector))
        # print(len(map))
        # print(len(cost_matrix))
        # print(len(pheromone_vector))
        # print(aco.get_edge_count(size))
        graph = aco.Graph(np.array(cost_matrix),np.array(pheromone_vector), np.array(heuristic_vector), size, size**2)
        algorithm = aco.AntColonyOpt(alpha, beta, evaporation, q, antNumber, modification, limit)
        # pl.show_heuristic(heuristic_map, 2 * (size - 1))
        cost, path = algorithm.run(graph, start, final)
        # print(path)
        xy_pathes.append([aco.get_vert_by_code(i, size) for i in path])
        # print(xy_path)
    tm = time.time() - startTime
    print(tm)
    times.append(tm)
    # pl.show_map(map, xy_pathes)
print(np.mean(times))
