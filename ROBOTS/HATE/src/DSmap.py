"""DSmap"""
import math
import numpy as np
from tools import get_mean

# from tools import get_conj
# from tools import get_distance_proj
# from tools import get_distance

class DSmap:
    """class for diamond square algorithm"""
    def __init__(self, n, m, R):
        self.n = n
        self.m = m
        self.max_element = pow(2, math.ceil(math.log(max(n, m) - 1, 2)))
        self.matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.height = (n + m) / 2
        self.max_dist_z = 0.0
        self.norm_matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.R = R

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

    def get_norm_matrix(self):
        return self.norm_matrix