
import numpy as np
from MPIalg import MPIalg
from MPIalg import ThomasAlg

def get_size():
    f=open("data/MPIparams.data", "r")
    n = np.int64(f.readline().strip().split("=")[1])
    return n

def test1(n):
    alg_obj = MPIalg(n=n)
    alg_obj.solve(filepath="data/MPIPythonTime.data")


def test2():
    alg_obj = MPIalg()
    alg_obj.read_data("data/test_matrix.data")
    alg_obj.solve()


n = get_size()
test1(n)
# test2()