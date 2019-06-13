"""Evolution algorithm implementation"""
import numpy as np
from graph import Graph
from tools import choice

class Ant:
    """Single ant behavior"""
    def __init__(self, graph: Graph, start, alpha, beta, q):
        self.graph = graph
        self.position = start
        self.alpha = alpha
        self.beta = beta
        self.path = [start]
        self.path_length = 0.0
        self.last_cost = 0.0
        self.q = q
        self.increase = [0.0]
        self.iteration = 0
        self.fail = False

    def get_pos(self):
        """Get ant's position"""
        return self.position

    def move(self):
        """Move ant in next graph's point"""
        available_moves, moves_pheromones, moves_heuristic_d, moves_heuristic_h, moves_costs = self.graph.get_pos_parameters(self.position)
        weights = []
        sum_w = 0.0
        for it in range(len(available_moves)):
            weight = moves_pheromones[it] ** self.alpha * moves_heuristic_d[it] ** self.beta * moves_heuristic_h[it]
            sum_w += weight
            weights.append(weight)
        weights = [w / sum_w for w in weights]
        choosen_idx = choice(weights)
        self.position = available_moves[choosen_idx]
        self.path.append(self.position)
        self.increase.append(moves_costs[choosen_idx])
        self.path_length += moves_costs[choosen_idx]
        self.iteration += 1

    def get_position(self):
        """Returns position of ant"""
        return self.position

    def get_pheromone_increase(self, idx):
        """Return pheromone increase for idx move"""
        return self.q / self.increase[idx]

    def get_path_length(self):
        """Returns path length"""
        return self.path_length

    def get_path(self):
        """Returns path"""
        return self.path

    def delete_loops(self):
        """Delete loops from path"""
        for it in self.path:
            if self.path.count(it) > 1:
                idx = self.path.index(it)
                for jt in range(idx, len(self.path) - 1 - self.path[::-1].index(it)): #last idx
                    self.path.pop(idx)
                    self.path_length -= self.increase[idx]

class EAlg:
    """Evolution algorithm"""
    def __init__(self, pop_size, iter_size, alpha, beta, rho, q):
        self.pop_size = pop_size
        self.iter_size = iter_size
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

    def get_path(self, graph: Graph, start: [], end_point: []):
        """Main method of algorithm, which find best path\n
        It returns cost and path
        """
        path = []
        path_length = float('inf')
        graph.init_pheromone_n_heuristics(end_point)
        lim = graph.get_size()[0] * graph.get_size()[1] / 10
        for it in range(self.iter_size):
            pheromone_increment = np.zeros(graph.get_size())
            for ant_it in range(self.pop_size):
                ant = Ant(graph, start, self.alpha, self.beta, self.q)
                while ant.get_pos() != end_point:
                    ant.move()
                    # if (ant.iteration == lim):
                    #     print(ant.path[len(ant.path) - 50:len(ant.path)])
                    #     ant.fail = True
                    #     quit()
                # if not ant.fail:
                pos = ant.get_pos()
                pheromone_increment[pos[0]][pos[1]] += ant.get_pheromone_increase(len(ant.get_path()) - 1)
                ant.delete_loops()
                if ant.get_path_length() < path_length:
                    path = ant.get_path()
                    path_length = ant.get_path_length()
            graph.update_pheromone(pheromone_increment, self.rho)
        return path, path_length
