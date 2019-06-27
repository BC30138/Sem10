import numpy as np


def get_edge_count(size):
    return 2 * size * (size - 1)


def get_edge_number(fstvert, sndvert, size):
    i = min([fstvert, sndvert])
    j = max([fstvert, sndvert])
    if j - i == 1:
        return i + i // size * (size - 1)
    if j - i == size:
        return i + j // size * (size - 1)
    print("smth wrong")
    return -1

def get_conj_vertices(vert , size):
    conj = []
    if vert % size != 0:
        conj.append(vert - 1)
    if vert >= size:
        conj.append(vert - size)
    if vert + size < size ** 2:
        conj.append(vert + size)
    if vert % size != size - 1:
        conj.append(vert + 1)
    return conj


def enumerate_map(map):
    enum = []
    for i in range(len(map)):
        for j in range(len(map)):
            enum.append(map[i][j])
    return enum

def get_vert_by_code(vert, size):
    i = 0
    while(vert >= size):
        vert -= size
        i += 1
    return [i, vert]

def get_code_by_vert(i, j, size):
    return i * size + j


# def unenumerate_map(map):
#     enum = []
#     for i in range(len(map)):
#         for j in range(len(map)):
#             enum.append(map[i][j])


class Graph:
    def __init__(self, costMatrix, pheromone, heuristic, size, vert_number):
        tau = 100
        self.costMatrix = costMatrix
        self.rank = vert_number
        self.mapSize = size
        # np.random.sample(len(costMatrix)) / tau +
        self.pheromone =  pheromone
        self.heuristic = heuristic

    def define_heuristic_value(self, available):
        heuristic = [self.heuristic[i] for i in available]
        minimum = min(heuristic)
        powers = [i - minimum for i in heuristic]
        denominator = sum([2 ** i for i in powers])
        heuristic = [2 ** i / denominator for i in powers]
        return heuristic

    def getrank(self):
        return self.rank

    def getMapSize(self):
        return self.mapSize

    def getcostmatrix(self):
        return self.costMatrix

    def updatepheromone(self, evaporation, ants):
        self.pheromone = self.pheromone * (1 - evaporation)
        for ant in ants:
            if ant.lost:
                continue
            self.pheromone += ant.getpheromone()

    def changelocal(self, vert, local):
        self.pheromone[vert] = (1 - local) * self.pheromone[vert] + local * 0.01 # constant t0 = sup(starting pheromone)

    def changeglobal(self, rho, path, cost):
        for i in range(len(self.pheromone)):
            self.pheromone[i] = (1 - rho) * self.pheromone[i]
        pherfunction = 1 / cost
        for i in path:
            # phn = get_edge_number(path[i], path[i+1], self.mapSize)
            self.pheromone[i] += pherfunction * rho


class Ant:
    def __init__(self, vertex, size):
        self.vertex = vertex
        self.path = [vertex]
        self.available = get_conj_vertices(vertex , size)
        self.cost = float(0)
        self.bitpheromone = []
        self.iteration = 0
        self.lost = False

    def getpheromone(self):
        return self.bitpheromone

    def movetonext(self, Graph, alpha, beta):
        stochastic = np.array([])
        moveto = self.vertex

        # print(self.available)
        heuristic_dir = Graph.define_heuristic_value(self.available)
        for i in range(len(self.available)):
            hr = get_edge_number(self.vertex, self.available[i], Graph.getMapSize())
            heuristic_h = 1 - Graph.getcostmatrix()[hr]
            # print(phn, "pher", Graph.pheromone[phn])
            stochastic = np.append(stochastic, Graph.pheromone[self.available[i]] ** alpha * heuristic_dir[i] ** beta * heuristic_h)
        stochastic = stochastic / stochastic.sum()
        # print(stochastic)
        #probabilities
        randvalue = np.random.sample()
        for vertexnumb, probability in enumerate(stochastic):
            randvalue -= probability
            if randvalue <= 0:
                moveto = self.available[vertexnumb]
                break
        # print(moveto)
        cstn = get_edge_number(self.vertex, moveto, Graph.getMapSize())
        self.cost += Graph.getcostmatrix()[cstn]
        self.available = get_conj_vertices(moveto, Graph.getMapSize())
        self.available.remove(self.vertex)
        self.vertex = moveto
        self.path = self.path + [moveto]
        self.iteration += 1
        # print(moveto)

    def changepheromone(self, Graph, strategy, q):
        self.bitpheromone = [0 for i in range(Graph.getrank())]
        for k in self.path:
            # i = self.path[k - 1]
            # j = self.path[k]
            # phn = get_edge_number(i, j, Graph.getMapSize())
            if strategy == 0:  # ant-quality system
                self.bitpheromone[k] = q
            elif strategy == 1:  # ant-density system
                # noinspection PyTypeChecker
                self.bitpheromone[k] = q / Graph.getcostmatrix()[k]
            else:  # ant-cycle system
                self.bitpheromone[k] = q / self.cost

    def calculateCost(self, Graph):
        cost = 0
        for i in range(len(self.path) - 1):
            cstn = get_edge_number(self.path[i], self.path[i+1], Graph.getMapSize())
            cost += Graph.getcostmatrix()[cstn]
        self.cost = cost


    def deleteLoops(self, Graph):
        # print(self.path)
        for i in self.path:
            if self.path.count(i) > 1:
                idx = self.path.index(i)
                for j in range(idx, len(self.path) - 1 - self.path[::-1].index(i)): #last idx
                    self.path.pop(idx)
        self.calculateCost(Graph)




class AntColonyOpt:
    """
    alpha - the concentration of pheromones
    beta - the weight of heuristic information
    evaporation - the evaporation rate
    q - positive constant
    modification - the one of the modifications AS: 0 - Ant-cycle, 1 - Ant-density, 2 - Ant-quantity
    limit - maximum number of iterations
    """
    def __init__(self, alpha, beta, evaporation, q, antNumber, modification, limit):
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.q = q
        self.antNumber = antNumber
        self.modification = modification
        self.limit = limit

    def run(self, Graph, start, final):
        cost = float('inf')
        path = []
        limit = Graph.getMapSize() ** 2 /10
        for iteration in range(self.limit):
            ants = [Ant(start, Graph.getMapSize()) for i in range(self.antNumber)]
            for ant in ants:
                while ant.vertex != final:
                    ant.movetonext(Graph, self.alpha, self.beta)
                    if (ant.iteration == limit):
                        break
                if (ant.iteration == limit):
                    ant.lost = True
                    continue
                # print("TUT")
                ant.deleteLoops(Graph)
                if ant.cost < cost:
                    cost = ant.cost
                    path = ant.path
                ant.changepheromone(Graph, self.modification, self.q)
            Graph.updatepheromone(self.evaporation, ants)
            # print(path)
        # print(cost, path)
        return cost, path