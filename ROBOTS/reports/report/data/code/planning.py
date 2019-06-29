"""Planning algorithm"""
from time import time
import numpy as np
from graph import Graph
from ant import EAlg
from tools import get_distance_proj

def planning(prog_bar_it, bar_, graph: Graph, model: EAlg, number_of_targets):
    """Returns list with robot's paths to targets and list of lenghts this paths"""
    robots = []
    targets = []
    x_max, y_max = graph.get_size()

    for it in range(number_of_targets):
        while True:
            robot = [np.random.randint(low=0, high=x_max),
                     np.random.randint(low=0, high=y_max)]
            if robot not in robots:
                if robot not in targets:
                    robots.append(robot)
                    break
        while True:
            target = [np.random.randint(low=0, high=x_max),
                      np.random.randint(low=0, high=y_max)]
            if target not in robots:
                if target not in targets:
                    targets.append(target)
                    break

    costs = [[0.0 for x in range(number_of_targets)] for y in range(number_of_targets)]
    for it in range(number_of_targets):
        for jt in range(number_of_targets):
            costs[it][jt] = get_distance_proj(robots[it], targets[jt])

    time_dic = {}

    plan_start = time()

    opt_paths = []
    opt_costs = []
    opt_pairs = []

    have_pair = np.zeros(number_of_targets)
    while not all(have_pair):
        it = 0
        while True:
            if not have_pair[it]:
                idx = costs[it].index(min(costs[it]))
                cost = costs[it][idx]
                if cost == min([row[idx] for row in costs]):
                    opt_pairs.append([it, idx])
                    have_pair[it] = True
                    costs[it] = [float('inf') for it in range(number_of_targets)]
                    for jt in range(number_of_targets):
                        costs[jt][idx] = float('inf')
                    break
                else: it += 1
            else: it += 1

    ant_start = time()
    time_dic["Planning"] = round(ant_start - plan_start, 3)

    for pair in opt_pairs:
        prog_bar_it[0] += 1
        bar_[0].update(prog_bar_it[0])
        path, cost = model.get_path(graph, robots[pair[0]], targets[pair[1]])
        opt_paths.append(path)
        opt_costs.append(cost)



    time_dic["AntColony"] = time() - ant_start
    time_dic["Whole"] = round(time_dic["AntColony"] + time_dic["Planning"], 3)

    return opt_paths, opt_costs, time_dic
