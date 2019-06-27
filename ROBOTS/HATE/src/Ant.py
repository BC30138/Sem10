import numpy as np
from tools import get_conj
from tools import choice
from tools import get_edge_number

class Ant:
    def __init__(self, vertex, size):
        self.vertex = vertex
        self.path = [vertex]
        self.available_moves = get_conj(vertex, size)
        self.iteration = 0
        self.cost = float(0)
        self.pheromone = []
        self.fail = False

    def get_pheromone(self):
        return self.pheromone

    def move_to_next(self, Graph, alpha, beta):
        weights = []
        sum_w = 0.0
        next_vertex = 0
        heuristic_dir = Graph.define_heuristic_value(self.available_moves)
        for i in range(len(self.available_moves)):
            hr = get_edge_number(self.vertex, self.available_moves[i], Graph.get_map_size())
            heuristic_h = 1 - Graph.get_cost_matrix()[hr]
            weight = Graph.pheromone[self.available_moves[i]] ** alpha * heuristic_dir[i] ** beta * heuristic_h
            weights.append(weight)
            sum_w += weight
        weights = [w / sum_w for w in weights]
        next_vertex = self.available_moves[choice(weights)]
        cstn = get_edge_number(self.vertex, next_vertex, Graph.get_map_size())

        self.cost += Graph.get_cost_matrix()[cstn]
        self.available_moves = get_conj(next_vertex, Graph.get_map_size())
        self.available_moves.remove(self.vertex)
        self.vertex = next_vertex
        self.path = self.path + [next_vertex]
        self.iteration += 1

    def change_pheromone(self, Graph, q):
        self.pheromone = [0 for i in range(Graph.get_rank())]
        for k in self.path:
            try:
                self.pheromone[k] = q / self.cost
            except ZeroDivisionError:
                self.pheromone[k] = 0.01

    def calc_cost(self, Graph):
        cost = 0
        for i in range(len(self.path) - 1):
            cstn = get_edge_number(self.path[i], self.path[i+1], Graph.get_map_size())
            cost += Graph.get_cost_matrix()[cstn]
        self.cost = cost

    def delete_loops(self, Graph):
        for i in self.path:
            if self.path.count(i) > 1:
                idx = self.path.index(i)
                for j in range(idx, len(self.path) - 1 - self.path[::-1].index(i)): #last idx
                    self.path.pop(idx)
        self.calc_cost(Graph)
