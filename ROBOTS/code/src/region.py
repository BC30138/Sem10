"""Region class"""
import random
import math
import numpy as np
from progress.bar import Bar

class Region:
    """class for diamond square algorithm"""
    def __init__(self, n, m, R):
        self.n = n
        self.m = m
        self.max_element = pow(2, math.ceil(math.log(max(n, m) - 1, 2)))
        self.matrix = np.zeros((self.max_element + 1, self.max_element + 1))
        self.height = (n + m) / 2
        self.noise = self.max_element * R
        self.rec_approx = 0.3 * pow(self.max_element + 1, 2) + 0.8 * self.max_element

    def generate(self):
        """main method"""
        self.matrix[0][0] = random.random() * self.height
        self.matrix[self.max_element][self.max_element] = random.random() * self.height
        self.matrix[self.max_element][0] = random.random() * self.height
        self.matrix[0][self.max_element] = random.random() * self.height

        side_length = self.max_element
        progress_h = int(self.rec_approx / 100) + 1
        mess = 'Generating matrix with size: {}x{}'.format(self.n, self.m)
        iter = 0
        with Bar(mess, max = 100,  suffix='%(percent)d%%') as bar:
            while side_length != 1:
                x_1 = 0
                y_1 = 0
                x_2 = side_length
                y_2 = side_length
                while True:
                    iter += 1
                    if (iter % progress_h) == 0:
                        bar.next()
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
            bar.finish
        self.matrix = self.matrix[0:self.n, 0:self.m]
        self.matrix = np.around(self.matrix, decimals=3)

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






