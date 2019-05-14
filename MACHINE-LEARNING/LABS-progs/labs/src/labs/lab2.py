"""lab2: KNN"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import tools as tls

def my_distance(weights):
    print(weights)
    return weights

def tic_tac_toe():
    """'Tic-tac-toe' data-set"""
    data = tls.MLStructure()
    data_frame = pd.read_csv('data/Tic_tac_toe.txt', header=None)
    data.x, data.y = tls.tic_tac_toe_prep_get_x_y(data_frame)

    data.split_data_into_test_train(0.2)
    # kde = KernelDensity(kernel="epanechnikov").fit(data.x_train)
    # print(kde.score_samples(data.x_train))
    data.my_distance(data.x_train)
    # data.clf = KNeighborsClassifier(n_neighbors=25, weights=data.my_distance)
    # data.clf = KNeighborsClassifier(n_neighbors=25)
    # data.classify()

    # accuracy_list = data.get_accuracy_volume_dependency(0.1, 0.8, 10)
    # tls.plot_precision(accuracy_list, 'results/KNN/tic_tac_toe.png')

    # data.split_data_into_test_train(0.2)
    # data.classify()
    # data.show_stat()