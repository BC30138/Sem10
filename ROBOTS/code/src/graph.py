"""Graph class"""
import math
import numpy as np
from tools import get_conj
from tools import get_distance_proj
from tools import get_distance
from tools import get_mean

class Graph:
    """class for diamond square algorithm"""
    def __init__(self, n, m, R, pheromone_eur_par):
        self.n = n
        self.m = m
        self.max_element = pow(2, math.ceil(math.log(max(n, m) - 1, 2)))
        self.matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.norm_matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.height = (n + m) / 2
        self.pheromone_eur_par = pheromone_eur_par
        self.max_dist_z = 0.0
        self.max_dist_x_y = get_distance_proj([0, 0], [self.n - 1, self.m - 1])
        self.available_moves = [[float(0) for x in range(n)] for y in range(m)]
        self.heuristic_h = [[float(0) for x in range(n)] for y in range(m)]
        self.costs = [[float(0) for x in range(n)] for y in range(m)]
        self.heuristic_d = np.zeros((n, m))
        self.pheromone = np.ones((n, m))
        self.R = R
        self.first_call = True

    def generate(self):
        """main method"""
        self.matrix[0][0] = np.random.uniform(low=0, high=self.height)
        self.matrix[self.max_element][self.max_element] = np.random.uniform(low=0, high=self.height)
        self.matrix[self.max_element][0] = np.random.uniform(low=0, high=self.height)
        self.matrix[0][self.max_element] = np.random.uniform(low=0, high=self.height)

        side_length = self.max_element
        while side_length != 1:
            x_1 = 0
            y_1 = 0
            x_2 = side_length
            y_2 = side_length
            while True:
                self.square(x_1, y_1, x_2, y_2)
                self.diamond(x_1, y_1, x_1, y_2)
                self.diamond(x_1, y_2, x_2, y_2)
                self.diamond(x_2, y_2, x_2, y_1)
                self.diamond(x_2, y_1, x_1, y_1)
                if y_2 == self.max_element:
                    if x_2 == self.max_element:
                        break
                    else:
                        x_1 += side_length
                        x_2 += side_length
                        y_1 = 0
                        y_2 = side_length
                else:
                    y_1 += side_length
                    y_2 += side_length
            side_length = int(side_length / 2)
        self.matrix = self.matrix[0:self.n, 0:self.m]
        self.matrix = np.around(self.matrix, decimals=3)
        self.max_dist_z = np.amax(self.matrix) - np.amin(self.matrix)
        self.norm_matrix = self.matrix - np.amin(self.matrix)
        self.norm_matrix = self.norm_matrix / self.max_dist_z

    def square(self, x_1, y_1, x_2, y_2):
        """square step of algorithm"""
        rad = (x_2 - x_1) / 2
        center_x = int(x_1 + rad)
        center_y = int(y_1 + rad)
        vertexes = [self.matrix[x_1][y_1],
                    self.matrix[x_2][y_2],
                    self.matrix[x_1][y_2],
                    self.matrix[x_2][y_1]]
        self.matrix[center_x][center_y] = (get_mean(vertexes)) + np.random.uniform(low=(- self.R * rad * 2), high=(self.R * rad * 2))

    def diamond(self, x_1, y_1, x_2, y_2):
        """diamond step of algorithm"""
        vertexes = []
        x = 0
        y = 0
        rad = 0.0
        if x_1 == x_2:
            center_y = int((y_1 + y_2) / 2)
            rad = abs(y_2 - center_y)
            if x_1 not in (0, self.max_element):
                vertexes += [self.matrix[x_1][y_1],
                             self.matrix[x_2][y_2],
                             self.matrix[x_1 - rad][center_y],
                             self.matrix[x_1 + rad][center_y]]
            else:
                if x_1 == 0:
                    vertexes += [self.matrix[x_1][y_1],
                                 self.matrix[x_2][y_2],
                                 self.matrix[x_1 + rad][center_y]]
                if x_1 == self.max_element:
                    vertexes += [self.matrix[x_1][y_1],
                                 self.matrix[x_2][y_2],
                                 self.matrix[x_1 - rad][center_y]]
            x = x_1
            y = center_y
        else:
            center_x = int((x_1 + x_2) / 2)
            rad = abs(x_2 - center_x)
            if y_1 not in (0, self.max_element):
                vertexes += [self.matrix[x_1][y_1],
                             self.matrix[x_2][y_2],
                             self.matrix[center_x][y_1 - rad],
                             self.matrix[center_x][y_1 + rad]]
            else:
                if y_1 == 0:
                    vertexes += [self.matrix[x_1][y_1],
                                 self.matrix[x_2][y_2],
                                 self.matrix[center_x][y_1 + rad]]
                if y_1 == self.max_element:
                    vertexes += [self.matrix[x_1][y_1],
                                 self.matrix[x_2][y_2],
                                 self.matrix[center_x][y_1 - rad]]
            x = center_x
            y = y_1
        self.matrix[x][y] = get_mean(vertexes) + np.random.uniform(low=(- self.R * rad * 2), high=(self.R * rad * 2))

    def get_size(self):
        """Get size of graph in format (,)"""
        return (self.n, self.m)

    def init_pheromone_n_heuristics(self, end_point):
        """Init pheromone matrix, heuristic_d matrix, heuristic_h matrix of distances to available \n
            moves by z and available_moves matrix of lists"""
        if self.first_call:
            for it in range(self.n):
                for jt in range(self.m):
                    dist_to_conj = []
                    conj_points = get_conj(self.norm_matrix, [it, jt])
                    for point in conj_points:
                        dist_to_conj.append(get_distance([it, jt], point, self.matrix))
                    self.costs[it][jt] = dist_to_conj
                    self.available_moves[it][jt] = conj_points
            self.first_call = False
        else:
            self.heuristic_h = [[float(0) for x in range(self.n)] for y in range(self.m)]
            self.heuristic_d = np.zeros((self.n, self.m))
            self.pheromone = np.ones((self.n, self.m))

        end_point_val = max(self.n, self.m)
        for it in range(self.n):
            for jt in range(self.m):
                if not (it == end_point[0] and jt == end_point[1]):
                    pheromone = 1 - (get_distance_proj([it, jt], end_point) / self.max_dist_x_y + np.random.uniform(- self.pheromone_eur_par, self.pheromone_eur_par))
                    if pheromone < 0:
                        self.pheromone[it][jt] = 0.0
                    else:
                        self.pheromone[it][jt] = pheromone
                z_dist_to_conj = []
                conj_points = get_conj(self.norm_matrix, [it, jt])
                for point in conj_points:
                    z_dist_to_conj.append(1 - abs(self.norm_matrix[point[0]][point[1]] - self.norm_matrix[it][jt]))
                self.heuristic_h[it][jt] = z_dist_to_conj
                self.heuristic_d[it][jt] = end_point_val - max(abs(it - end_point[0]), abs(jt - end_point[1]))

    def update_pheromone(self, pheromone_increment: np.array, evaporation_coef):
        """Updates pheromone values"""
        self.pheromone *= (1 - evaporation_coef)
        self.pheromone += pheromone_increment

    def get_pheromone(self, position):
        """Returns pheromone value for position"""
        return self.pheromone[position[0]][position[1]]

    def get_heuristic_h(self, position):
        """Returns list of distance by z to possible moves for ant"""
        return self.heuristic_h[position[0]][position[1]]

    def get_available_moves(self, position):
        """Returns list of possible moves for ant"""
        return self.available_moves[position[0]][position[1]]

    def get_heuristic_d(self, position):
        """Returns heuristic_d value for position"""
        return self.heuristic_d[position[0]][position[1]]

    def get_cost(self, position):
        """Returns list costs for conjugate positions"""
        return self.costs[position[0]][position[1]]

    def get_pos_parameters(self, position):
        """Returns parameters for possibility calculating \n
        return available_moves, pheromones, heuristic_d, self.get_heuristic_h(position)"""
        available_moves = self.get_available_moves(position)
        heuristic_d = []
        pheromones = []
        for move in available_moves:
            heuristic_d.append(self.get_heuristic_d(move))
            pheromones.append(self.get_pheromone(move))
        min_h_d = min(heuristic_d)
        heuristic_d = [val - min_h_d for val in heuristic_d]
        sum_d = sum([math.exp(w_d) for w_d in heuristic_d])
        heuristic_d = [math.exp(w_d) / sum_d for w_d in heuristic_d]
        return available_moves, pheromones, heuristic_d, self.get_heuristic_h(position), self.get_cost(position)

    def get_matrix(self):
        """Returns surface in matrix formats"""
        return self.matrix
