"""Planning algorithm"""
from time import time
import numpy as np
from tools import get_coord
from tools import get_distance

def planning(size, model, number_of_targets):
    """Returns list with robot's paths to targets and list of lenghts this paths"""
    robots = []
    targets = []

    for it in range(number_of_targets):
        while True:
            robot = np.random.randint(low=0, high=size ** 2)
            if robot not in robots:
                robots.append(robot)
                break
        while True:
            target = np.random.randint(low=0, high=size ** 2)
            if target not in (targets and robots):
                targets.append(target)
                break

    time_dic = {}
    ant_start = time()

    costs = [[0.0 for x in range(number_of_targets)] for y in range(number_of_targets)]
    for it in range(number_of_targets):
        for jt in range(number_of_targets):
            costs[it][jt] = get_distance(get_coord(robots[it], size), get_coord(targets[jt], size), model.map_)

    plan_start = time()
    time_dic["AntColony"] = round(plan_start - ant_start, 3)

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

    print(len(opt_pairs))
    for pair in opt_pairs:
        cost, path = model.run(robots[pair[0]], targets[pair[1]])
        opt_paths.append([get_coord(it, size) for it in path])
        opt_costs.append(cost)


    time_dic["Planning"] = round(time() - plan_start, 7)
    time_dic["Whole"] = round(time_dic["AntColony"] + time_dic["Planning"], 3)

    return opt_paths, opt_costs, time_dic
