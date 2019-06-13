"""Planning algorithm"""
import numpy as np
from graph import Graph

def planning(graph: Graph, model, number_of_targets):
    """Returns list with robot's paths to targets"""
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
            if target not in targets:
                targets.append(target)
                break


