class Graph:
    def __init__(self, costMatrix, pheromone, heuristic, size, vert_number):
        tau = 100
        self.costMatrix = costMatrix
        self.rank = vert_number
        self.mapSize = size
        self.pheromone =  pheromone
        self.heuristic = heuristic

    def define_heuristic_value(self, available):
        heuristic = [self.heuristic[i] for i in available]
        minimum = min(heuristic)
        powers = [i - minimum for i in heuristic]
        denominator = sum([2 ** i for i in powers])
        heuristic = [2 ** i / denominator for i in powers]
        return heuristic

    def get_rank(self):
        return self.rank

    def get_map_size(self):
        return self.mapSize

    def get_cost_matrix(self):
        return self.costMatrix

    def update_pheromone(self, evaporation, ants):
        self.pheromone = self.pheromone * (1 - evaporation)
        for ant in ants:
            if ant.fail:
                continue
            self.pheromone += ant.get_pheromone()

    def change_local(self, vert, local):
        self.pheromone[vert] = (1 - local) * self.pheromone[vert] + local * 0.01 # constant t0 = sup(starting pheromone)

    def change_global(self, rho, path, cost):
        for i in range(len(self.pheromone)):
            self.pheromone[i] = (1 - rho) * self.pheromone[i]
        pherfunction = 1 / cost
        for i in path:
            self.pheromone[i] += pherfunction * rho
