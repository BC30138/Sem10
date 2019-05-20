"""lab3: Decision Tree"""
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import tools as tls

data = tls.MLStructure()

def titanic():
    """titanic dataset"""
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tls.titanic_preprocessing(train_set)
    data.x_train, data.y_train = tls.titanic_get_train_x_y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    data.x_test = tls.titanic_preprocessing(x_test_set)
    data.y_test = y_test_set['Survived']

    data.clf = DecisionTreeClassifier(max_depth=3, max_leaf_nodes=5) # идеальное дерево 3 - 5

    data.classify()
    data.show_stat()

    tls.plot_tree(data, 'results/Tree/titanic_tree.png')

def glass():
    """glass dataset"""
    data_frame = pd.read_csv('data/glass.data', header=None)
    data.x_train, data.y_train = tls.glass_get_x_y(data_frame)
    data.x_test = np.reshape([1.516, 11.7, 1.01, 1.19, 72.59, 0.43, 11.44, 0.02, 0.1], (1, -1))

    data.clf = DecisionTreeClassifier(max_depth=32, max_leaf_nodes=32)
    data.clf.fit(data.x_train, data.y_train)
    data.y_result = data.clf.predict_proba(data.x_test)
    print(data.y_result)
    tls.plot_tree(data, 'results/Tree/glass_tree_full.png')

    data.clf = DecisionTreeClassifier(max_depth=4, max_leaf_nodes=17)
    data.clf.fit(data.x_train, data.y_train)
    data.y_result = data.clf.predict_proba(data.x_test)
    print(data.y_result)
    tls.plot_tree(data, 'results/Tree/glass_tree_opt.png')
