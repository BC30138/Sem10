"""Graph class"""
import random
import math
import numpy as np
from tools import get_conj
from tools import get_distance

class Graph:
    """class for diamond square algorithm"""
    def __init__(self, n, m, R):
        self.n = n
        self.m = m
        self.max_element = pow(2, math.ceil(math.log(max(n, m) - 1, 2)))
        self.matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.height = (n + m) / 2
        self.noise = self.max_element * R
        self.max_dist_z = 0.0
        self.costs = [[float(0) for x in range(self.max_element + 1)] for y in range(self.max_element + 1)]
        self.available_moves = [[float(0) for x in range(self.max_element + 1)] for y in range(self.max_element + 1)]
        self.pheromone = [[float(0) for x in range(self.max_element + 1)] for y in range(self.max_element + 1)]

    def generate(self):
        """main method"""
        self.matrix[0][0] = random.random() * self.height
        self.matrix[self.max_element][self.max_element] = random.random() * self.height
        self.matrix[self.max_element][0] = random.random() * self.height
        self.matrix[0][self.max_element] = random.random() * self.height

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

        self.generate_costs_and_moves()

    def square(self, x_1, y_1, x_2, y_2):
        """square step of algorithm"""
        center_x = int((x_1 + x_2) / 2)
        center_y = int((y_1 + y_2) / 2)
        nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[x_1][y_2] + self.matrix[x_2][y_1]
        self.matrix[center_x][center_y] = (nodes_sum / 4) + random.random() * (2 * self.noise) - self.noise

    def diamond(self, x_1, y_1, x_2, y_2):
        """diamond step of algorithm"""
        if x_1 == x_2:
            center_y = int((y_1 + y_2) / 2)
            rad = abs(y_2 - center_y)
            if x_1 not in (0, self.max_element):
                nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[x_1 - rad][center_y] + self.matrix[x_1 + rad][center_y]
                self.matrix[x_1][center_y] = (nodes_sum / 4) + random.random() * (2 * self.noise) - self.noise
            else:
                if x_1 == 0:
                    nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[x_1 + rad][center_y]
                    self.matrix[x_1][center_y] = (nodes_sum / 3) + random.random() * (2 * self.noise) - self.noise
                if x_1 == self.max_element:
                    nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[x_1 - rad][center_y]
                    self.matrix[x_1][center_y] = (nodes_sum / 3) + random.random() * (2 * self.noise) - self.noise
        else:
            center_x = int((x_1 + x_2) / 2)
            rad = abs(x_2 - center_x)
            if y_1 not in (0, self.max_element):
                nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[center_x][y_1 - rad] + self.matrix[center_x][y_1 + rad]
                self.matrix[center_x][y_1] = (nodes_sum / 4) + random.random() * (2 * self.noise) - self.noise
            else:
                if y_1 == 0:
                    nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[center_x][y_1 + rad]
                    self.matrix[center_x][y_1] = (nodes_sum / 3) + random.random() * (2 * self.noise) - self.noise
                if y_1 == self.max_element:
                    nodes_sum = self.matrix[x_1][y_1] + self.matrix[x_2][y_2] + self.matrix[center_x][y_1 - rad]
                    self.matrix[center_x][y_1] = (nodes_sum / 3) + random.random() * (2 * self.noise) - self.noise

    def generate_costs_and_moves(self):
        """Cost is distance by z between point and conjugate point"""
        for it in range(self.matrix.shape[0]):
            for jt in range(self.matrix.shape[1]):
                costs_to_conj = []
                conj_points = get_conj(self.matrix, [it, jt])
                for point in conj_points:
                    costs_to_conj.append(abs(self.matrix[point[0]][point[1]] - self.matrix[it][jt]))
                self.costs[it][jt] = (costs_to_conj)
                self.available_moves[it][jt] = conj_points

    def get_size(self):
        """Get size of graph in format (,)"""
        return (self.matrix.shape[0], self.matrix.shape[1])

    def init_pheromone(self, final):
        for it in range(self.matrix.shape[0]):
            for jt in range(self.matrix.shape[1]):
                if it == final[0] and jt == final[1]:
                    self.pheromone[it][jt] = float('inf')
                else:
                    self.pheromone[it][jt] = get_distance([it, jt], final)
