"""main file"""
import region
import tools
import numpy as np

def test_main():
    """function for testing"""
    n = 25
    n_robots_tasks = 5
    test = region.Region(n, n, 0.04)
    test.generate()
    tools.surface_plot(test.matrix, "data/test.png")



test_main()
