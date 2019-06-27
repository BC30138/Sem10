import numpy as np
from tools import to_vector
from tools import get_coord
from tools import get_distance_square_proj
from tools import plot_heuristic
from tools import plot_pheromone
from Ant import Ant
from Graph import Graph

class AntColony:
    def __init__(self, map_obj, start_noise_pher, alpha, beta, evap, q, pop_size, iter_num):
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evap
        self.q = q
        self.pop_size = pop_size
        self.size = map_obj.size
        self.start_noise_pher = start_noise_pher
        self.map_ = map_obj.get_norm_map()
        self.iter_num = iter_num

    def run(self, start, final):
        cost = float('inf')
        path = []
        # plot_pheromone(self.create_pheromone(start, final), "data/init/p_test.png")
        # plot_heuristic(self.create_heuristic(final), "data/init/h_test.png")
        pheromone_vector = to_vector(self.create_pheromone(start, final))
        heuristic_vector = to_vector(self.create_heuristic(final))
        cost_matrix = self.get_cost_vector()
        graph = Graph(np.array(cost_matrix), np.array(pheromone_vector), np.array(heuristic_vector),
                      self.size, self.size ** 2)
        limit = self.size ** 2 / 10
        for iteration in range(self.iter_num):
            ants = [Ant(start, self.size) for i in range(self.pop_size)]
            for ant in ants:
                while ant.vertex != final:
                    ant.move_to_next(graph, self.alpha, self.beta)
                    if (ant.iteration == limit):
                        ant.fail = True
                        break
                if not ant.fail:
                    ant.delete_loops(graph)
                    if ant.cost < cost:
                        cost = ant.cost
                        path = ant.path
                    ant.change_pheromone(graph, self.q)
            graph.update_pheromone(self.evaporation, ants)

        return cost, path

    def create_pheromone(self, start, final):
        pheromone_map = np.ones((self.size, self.size))
        final_coord = get_coord(final, self.size)
        for x in range(self.size):
            for y in range(self.size):
                if not (x == final_coord[0] and y == final_coord[1]):
                    pheromone = 1 - (get_distance_square_proj([x, y], final_coord) /
                        (2 * self.size ** 2) + np.random.uniform(- self.start_noise_pher, self.start_noise_pher))
                    if pheromone < 0:
                        pheromone_map[x][y] = 0.0
                    else:
                        pheromone_map[x][y] = pheromone
        return pheromone_map

    def create_heuristic(self, final):
        heuristic_map = np.zeros((self.size, self.size))
        final_coord = get_coord(final, self.size)
        for x in range(self.size):
            for y in range(self.size):
                heuristic_map[x][y] = self.size - max(abs(x - final_coord[0]), abs(y - final_coord[1]))
        return heuristic_map

    def get_cost_vector(self):
        cost_vector = []
        for it in range(len(self.map_) - 1):
            for jt in range(len(self.map_) - 1):
                cost_vector.append(abs(self.map_[it][jt] - self.map_[it][jt + 1]))
            for jt in range(len(self.map_)):
                cost_vector.append(abs(self.map_[it][jt] - self.map_[it + 1][jt]))
        for jt in range(len(self.map_) - 1):
            cost_vector.append(abs(self.map_[len(self.map_) - 1][jt] - self.map_[len(self.map_) - 1][jt + 1]))
        return cost_vector
