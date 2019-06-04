"""main file"""
import numpy as np
import tools
from region import Region
from ant import AntsAlg

def test_main():
    """function for testing"""
    n = 5
    # n_robots_tasks = 5
    region = Region(n, n, 0.02)
    region.generate()
    tools.surface_plot(region.matrix, "data/test_grid.png")
    ants_alg = AntsAlg(region, 10, 10, 0.0, 0.9)
    path, length, res_time = ants_alg.generate((0, 0), (4, 4))
    print(res_time)
    tools.plot_path(region.matrix, path, "data/test_path.png")
    # print([region.matrix[x] for x in path])

test_main()