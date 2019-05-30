"""Region class"""
import numpy as np
import random

class Region:
    """class for diamond square algorithm"""
    def __init__(self, n, height, R):
        self.size = pow(2, n) + 1
        self.matrix = np.zeros((self.size, self.size))
        self.height = height
        self.noise = self.size * R
        self.size -= 1

    def generate(self):
        self.matrix[0][0] = random.random() * self.height
        self.matrix[self.size][self.size] = random.random() * self.height
        self.matrix[self.size][0] = random.random() * self.height
        self.matrix[0][self.size] = random.random() * self.height
        self.square(0, int(self.size))
        print(self.matrix)

    def square(self, top, bottom):
        center = int((top + bottom) / 2)
        sum = self.matrix[top][top] + self.matrix[bottom][bottom] + self.matrix[top][bottom] + self.matrix[bottom][top]
        self.matrix[center][center] = (sum / 4) + random.random() * (2 * self.noise) - self.noise

    def diamond(self, top, bottom):
        center = int((top + bottom) / 2)

