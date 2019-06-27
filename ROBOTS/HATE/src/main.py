from DSmap import DSmap
from tools import to_vector

def test():


size = 5

R_for_DS = 0.02
dsmap = DSmap(size, size, R_for_DS)
dsmap.generate()

map_for_calc = dsmap.get_norm_matrix()
map_for_calc = to_vector(map_for_calc)


print(map_for_calc)