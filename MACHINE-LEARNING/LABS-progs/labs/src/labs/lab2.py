"""lab2: KNN"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
# from sklearn.neighbors import KNeighborsClassifier
import tools as tls

# def my_kernel(X, Y):
#     """
#     We create a custom kernel:

#                  (2  0)
#     k(X, Y) = X  (    ) Y.T
#                  (0  1)
#     """
#     M = np.array([[2, 0], [0, 1.0]])
#     return np.dot(np.dot(X, M), Y.T)

def tic_tac_toe():
    """'Tic-tac-toe' data-set"""
    data = tls.MLStructure()
    data_frame = pd.read_csv('data/Tic_tac_toe.txt', header=None)
    data.x, data.y = tls.tic_tac_toe_prep_get_x_y(data_frame)

    data.clf = KNeighborsClassifier(n_neighbors=25, weights='distance')

    accuracy_list = data.get_accuracy_volume_dependency(0.1, 0.8, 10)
    tls.plot_precision(accuracy_list, 'results/KNN/tic_tac_toe.png')

    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()