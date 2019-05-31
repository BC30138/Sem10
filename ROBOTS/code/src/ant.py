import numpy as np

class antsalg:
    """object with everithing necessary for ant algorithm"""
    def __init__(self, region):
        self.matrix = region.matrix

    def get_path(self):
