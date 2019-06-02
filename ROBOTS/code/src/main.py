"""main file"""
import numpy as np
import tools
from region import Region
from ant import AntsAlg

def test_main():
    """function for testing"""
    n = 5
    # n_robots_tasks = 5
    region = Region(n, n, 0.04)
    region.generate()
    tools.surface_plot(region.matrix, "data/test.png")
    ants_alg = AntsAlg(region, 10, 50, 1.0, 0.9)
    path, length = ants_alg.generate((0, 0), (4, 4))
    print(path)
    print(length)


test_main()