"""Evolution algorithm implementation"""
import numpy as np
from graph import Graph

class Ant:
    """Single ant behavior"""
    def __init__(self, graph: Graph, start, pheromone):
        self.available_moves = graph.costs
        self.position = start
        pass



class EAlg:
    """Evolution algorithm"""
    def __init__(self, pop_size, iter_size, alpha, beta, rho, q):
        self.pop_size = pop_size
        self.iter_size = iter_size
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

    def get_path(self, graph: Graph, start, final):
        """Main method of algorithm, which find best path\n
        It returns cost and path
        """

        graph.init_pheromone(final)

        print(graph.get_pheromone())

        # for it in range(self.iter_size):
        #     for ant in range(self.pop_size):
        #         while





