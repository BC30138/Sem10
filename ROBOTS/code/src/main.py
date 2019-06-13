"""main file"""
from time import time
from tools import plot_map
from tools import plot_paths
from tools import plot_heuristic_d
from tools import plot_pheromone
from tools import plot_surface
from graph import Graph
from ant import EAlg

EALG_OBJ = EAlg(
    20,
    5,
    1.0,
    1.0,
    0.5,
    50
)

def main_test():
    """Main function \n
        Result of this I will use for report"""
    # sizes = (25, 50, 100, 250, 500, 1000)
    sizes = (5, 10)
    for size in sizes:
        for map_it in range(10):
            graph = Graph(size, size, 0.02, 0.1)
            graph.generate()

def examples_of_data():
    """Necessary for report"""
    size = 250
    graph = Graph(size, size, 0.05, 0.8)
    graph.generate()
    graph.init_pheromone_n_heuristics([50, 80])
    plot_heuristic_d(graph, "data/heuristics/heuristic_d.png")
    plot_pheromone(graph, "data/heuristics/pheromone.png")
    # plot_surface(graph, "data/surface.png")
    plot_map(graph, "data/maps/map_250.png")

def dev_test():
    """Function for development \n
        I use it for testing components"""
    size = 250
    graph = Graph(size, size, 0.3, 0.1)
    graph.generate()
    s_time = time()
    path_1, cost_1 = EALG_OBJ.get_path(graph, [1, 1], [100, 200])
    path_2, cost_2 = EALG_OBJ.get_path(graph, [100, 210], [23, 50])
    e_time = time()
    print(e_time - s_time)
    paths = [path_1, path_2]
    plot_map(graph, "data/maps/map_250.png")
    plot_paths(graph, paths, "data/path/test.png")

# examples_of_data()
dev_test()