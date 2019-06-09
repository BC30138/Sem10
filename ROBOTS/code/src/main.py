"""main file"""
import numpy as np
import tools
from graph import Graph
from ant import EAlg



def main_test():
    # sizes = (25, 50, 100, 250, 500, 1000)
    sizes = (5, 10)
    for size in sizes:
        for map_it in range(10):
            graph = Graph(size, size, 0.02)
            graph.generate()


def dev_test():
    size = 5
    graph = Graph(size, size, 0.02)
    graph.generate()
    ealg_obj = EAlg(
        50,
        5,
        1.0,
        1.0,
        0.9,
        50
    )
    ealg_obj.get_path(graph, [0, 0], [4, 4])

dev_test()
