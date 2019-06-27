from DSmap import DSmap
from AntColony import AntColony
from planning import planning
from tools import plot_paths

# def test():
size = 250
R_for_DS = 0.1

start_noise_pher = 0.0
alpha = 1
beta = 1
evap = 0.9
q = 50
pop_size = 50
iter_num = 10

def generate_map(size_, R_for_DS_):
    dsmap = DSmap(size_, R_for_DS_)
    dsmap.generate()
    return dsmap

map_obj = generate_map(size, R_for_DS)

AntAlgorithm = AntColony(map_obj, start_noise_pher, alpha, beta, evap, q, pop_size, iter_num)
# cost, path = AntAlgorithm.run(0, 180)
opt_paths, opt_costs, alg_time = planning(size, AntAlgorithm, 50)
plot_paths(map_obj, opt_paths, "data/path/test.png")

print(alg_time)
# print(map_obj.get_map_for_calc())
# print(cost)
# print(path)