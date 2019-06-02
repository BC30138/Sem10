"""Ant algorithm"""
import random
import math
import numpy as np
from tools import choice

import cProfile, pstats, io
from pstats import SortKey

class Pheromone:
    """pheromone store with map and values format"""
    def __init__(self):
        self.map = list()
        self.values = list()

    def set(self, el_map, el_val):
        """set value"""
        if el_map[0][0] > el_map[1][0]:
            swap = el_map[0]
            el_map[0] = el_map[1]
            el_map[1] = swap
        else:
            if el_map[0][0] == el_map[1][0]:
                if el_map[0][1] > el_map[1][1]:
                    swap = el_map[0]
                    el_map[0] = el_map[1]
                    el_map[1] = swap
        try:
            idx = self.map.index(el_map)
            self.values[idx] = el_val
        except ValueError:
            list.append(self.map, el_map)
            list.append(self.values, el_val)

    def plus_equal(self, el_map, val):
        """for updating"""
        actual_val = self.get(el_map)
        if len(self.map) > 65:
                a = 5
                pass
        self.set(el_map, actual_val + val)

    def get(self, el_map):
        """get val of el_map"""
        tmp = el_map
        if tmp[0][0] > tmp[1][0]:
            swap = tmp[0]
            tmp[0] = tmp[1]
            tmp[1] = swap
        else:
            if tmp[0][0] == tmp[1][0]:
                if tmp[0][1] > tmp[1][1]:
                    swap = tmp[0]
                    tmp[0] = tmp[1]
                    tmp[1] = swap
        try:
            idx = self.map.index(tmp)
            return self.values[idx]
        except ValueError:
            return 0.0

    def mult(self, right_val):
        """mult operator"""
        for value in self.values:
            value *= right_val

    def equal(self, new_map, new_val):
        """eq operator"""
        self.map = new_map
        self.values = new_val


class AntsAlg:
    """object with everithing necessary for ant algorithm"""
    def __init__(self, region, population_size, iter_num, alpha, rho):
        self.matrix = region.matrix
        self.population_size = population_size
        self.iter_num = iter_num
        self.alpha = alpha
        self.rho = rho

    def generate(self, start_point, end_point):
        """generate path and cost"""
        pheromone = Pheromone()
        best_path = list()
        best_length = float("inf")

        for iteration in range(self.iter_num):
            print(iteration)
            next_iteration_pheromone = Pheromone()
            next_iteration_pheromone.equal(pheromone.map, pheromone.values)
            next_iteration_pheromone.mult(1 - self.rho)
            for ant_it in range(self.population_size):
                path = list()
                path_length = 0.0
                current_position = start_point
                while current_position != end_point:
                    path.append(current_position)
                    possible_moves = self.get_possible_moves(path, current_position)
                    next_position = (0, 0)
                    if iteration == 0:
                        next_position = random.choice(possible_moves)
                    else:
                        moves_probabilities = self.get_probability(current_position, possible_moves, pheromone)
                        next_position = choice(possible_moves, moves_probabilities)
                    path_length += math.sqrt(pow(next_position[0] - current_position[0], 2)
                                             + pow(next_position[1] - current_position[1], 2)
                                             + pow(self.matrix[next_position] - self.matrix[current_position], 2))
                    next_iteration_pheromone.plus_equal([current_position, next_position], 1 / path_length)
                    current_position = next_position
                if path_length < best_length:
                    best_length = path_length
                    best_path = path
            pheromone = next_iteration_pheromone

        best_path.append(end_point)
        return best_path, best_length

    def get_probability(self, current_position, possible_moves, pheromone):
        """get array of probabilities for possible moves"""
        sum_ = 0
        moves_probabilities = np.empty((0))
        for move in possible_moves:
            influence = pow(pheromone.get([current_position, move]), self.alpha)
            moves_probabilities = np.append(moves_probabilities, influence)
            sum_ += influence
        if sum_ != 0:
            moves_probabilities = moves_probabilities / sum_
        else:
            moves_probabilities = np.ones(moves_probabilities.shape)
        return moves_probabilities


    def get_possible_moves(self, path, current_position):
        """get possible points pon grid for next step"""
        possible_moves = list()
        for it in range(current_position[0] - 1, current_position[0] + 2):
            for jt in range(current_position[1] - 1, current_position[1] + 2):
                list.append(possible_moves, (it, jt))

        top_del = False
        row_del = False
        del possible_moves[4]
        if current_position[0] in (0, self.matrix.shape[0] - 1):
            row_del = True
            if current_position[0] == 0:
                top_del = True
                del possible_moves[0:3]
            else:
                del possible_moves[5:]
        if current_position[1] in (0, self.matrix.shape[1] - 1):
            if current_position[1] == 0:
                if not row_del:
                    del possible_moves[0]
                    del possible_moves[2]
                    del possible_moves[3]
                else:
                    if top_del:
                        del possible_moves[0]
                        del possible_moves[1]
                    else:
                        del possible_moves[0]
                        del possible_moves[2]
            else:
                if not row_del:
                    del possible_moves[2]
                    del possible_moves[3]
                    del possible_moves[5]
                else:
                    if top_del:
                        del possible_moves[1]
                        del possible_moves[3]
                    else:
                        del possible_moves[2]
                        del possible_moves[3]

        not_deleted_moves = list()
        for pos in possible_moves:
            try:
                path.index(pos)
            except ValueError:
                list.append(not_deleted_moves, pos)
                pass

        if not not_deleted_moves:
            list.append(not_deleted_moves, random.choice(possible_moves))

        return not_deleted_moves
