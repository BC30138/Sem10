"""Planning algorithm"""
from time import time
import numpy as np
from graph import Graph
from ant import EAlg

def planning(graph: Graph, model: EAlg, number_of_targets):
    """Returns list with robot's paths to targets and list of lenghts this paths"""
    robots = []
    targets = []
    x_max, y_max = graph.get_size()
    for it in range(number_of_targets):
        while True:
            robot = [np.random.randint(low=0, high=x_max),
                     np.random.randint(low=0, high=y_max)]
            if robot not in robots:
                robots.append(robot)
                break
        while True:
            target = [np.random.randint(low=0, high=x_max),
                     np.random.randint(low=0, high=y_max)]
            if target not in (targets and robots):
                targets.append(target)
                break

    costs = [[0.0 for x in range(number_of_targets)] for y in range(number_of_targets)]
    paths = [[[] for x in range(number_of_targets)] for y in range(number_of_targets)]

    time_dic = {}

    ant_start = time()

    for it in range(number_of_targets):
        for jt in range(number_of_targets):
            paths[it][jt], costs[it][jt] = model.get_path(graph, robots[it], targets[jt])

    plan_start = time()
    time_dic["AntColony"] = round(plan_start - ant_start, 3)

    opt_paths = []
    opt_length = []

    while costs:
        it = 0
        while it < len(costs):
            idx = costs[it].index(min(costs[it]))
            cost = costs[it][idx]
            if cost == min([row[idx] for row in costs]):
                opt_paths.append(paths[it][idx])
                opt_length.append(costs[it][idx])
                del costs[it]
                del paths[it]
                for jt in range(len(costs)):
                    del costs[jt][idx]
                    del paths[jt][idx]
            else:
                it += 1

    time_dic["Planning"] = round(time() - plan_start, 7)
    time_dic["Whole"] = round(time_dic["AntColony"] + time_dic["Planning"], 3)

    return opt_paths, opt_length, time_dic
