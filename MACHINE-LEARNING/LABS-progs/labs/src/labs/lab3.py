"""lab3: Decision Tree"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import tools as tls

DATA = tls.MLStructure()

def glass():
    """glass dataset"""
    data_frame = pd.read_csv('data/glass.data', header=None)
    DATA.x_train, DATA.y_train = tls.glass_get_x_y(data_frame)
    DATA.x_test = np.reshape([1.516, 11.7, 1.01, 1.19, 72.59, 0.43, 11.44, 0.02, 0.1], (1, -1))

    DATA.clf = DecisionTreeClassifier(max_leaf_nodes=20)
    DATA.clf.fit(DATA.x_train, DATA.y_train)
    DATA.y_result = DATA.clf.predict_proba(DATA.x_test)
    print(DATA.y_result)
    tls.plot_tree(DATA, 'results/Tree/glass_tree_full.png')

    DATA.clf = DecisionTreeClassifier(max_depth=4, max_leaf_nodes=17)
    DATA.clf.fit(DATA.x_train, DATA.y_train)
    DATA.y_result = DATA.clf.predict_proba(DATA.x_test)
    print(DATA.y_result)
    tls.plot_tree_rotate(DATA, 'results/Tree/glass_tree_opt.png')

def spam7_daag():
    """spam7 DAAG dataset"""
    train_set = pd.read_csv('data/spam7DAAG.csv')
    DATA.x, DATA.y = tls.spam7_get_x_y(train_set)
    DATA.clf = DecisionTreeClassifier(max_leaf_nodes=8)

    DATA.clf.fit(DATA.x, DATA.y)
    tls.plot_tree_no_predict(DATA, 'results/Tree/spam7.png')

    DATA.split_data_into_test_train(0.1)
    accuracy_list = []
    for n_leafs in range(2, 10):
        acc_sum = 0
        DATA.clf = DecisionTreeClassifier(max_leaf_nodes=n_leafs)
        for it in range(5):
            DATA.classify()
            acc_sum += accuracy_score(DATA.y_test, DATA.y_result)
        accuracy_list.append([n_leafs, acc_sum / 5])
    tls.plot_tree_precision(np.array(accuracy_list), 'results/Tree/spam7_stat.png')

    DATA.clf = DecisionTreeClassifier(max_leaf_nodes=6)
    DATA.classify()
    DATA.show_stat()
    tls.plot_tree(DATA, 'results/Tree/spam7_opt.png')

def nsw74psid1_daag():
    """nsw74psid1 DAAG dataset"""
    train_set = pd.read_csv('data/nsw74psid1DAAG.csv')
    DATA.x, DATA.y = tls.nsw74psid1_get_x_y(train_set)
    DATA.clf = DecisionTreeRegressor(max_leaf_nodes=8)

    DATA.clf.fit(DATA.x, DATA.y)
    tls.plot_tree_regr(DATA, 'results/Tree/nsw74psid1.png')

def lenses():
    """lenses dataset"""
    train_set = pd.read_csv('data/lenses.data')
    DATA.x, DATA.y = tls.lenses_get_x_y(train_set)
    DATA.x_test = np.reshape([2, 1, 2, 1], (1, -1))
    DATA.clf = DecisionTreeClassifier(max_leaf_nodes=3)
    DATA.clf.fit(DATA.x, DATA.y)
    DATA.y_result = DATA.clf.predict_proba(DATA.x_test)
    print(DATA.y_result)
    tls.plot_tree_regr(DATA, 'results/Tree/lenses.png')

def svmdata():
    """svm dataset"""
    train_set = pd.read_csv('data/svmdata4.csv')
    test_set = pd.read_csv('data/svmdata4test.csv')
    DATA.x_train, DATA.y_train = tls.svmdata_get_x_y(train_set)
    DATA.x_test, DATA.y_test = tls.svmdata_get_x_y(test_set)

    DATA.clf = DecisionTreeClassifier(max_leaf_nodes=9)
    DATA.classify()
    DATA.show_stat()
    tls.plot_tree(DATA, 'results/Tree/svmdata.png')

def titanic():
    """titanic dataset"""
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tls.titanic_preprocessing(train_set)
    DATA.x_train, DATA.y_train = tls.titanic_get_train_x_y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    DATA.x_test = tls.titanic_preprocessing(x_test_set)
    DATA.y_test = y_test_set['Survived']

    DATA.clf = DecisionTreeClassifier(max_depth=3, max_leaf_nodes=5) # идеальное дерево 3 - 5

    DATA.classify()
    DATA.show_stat()

    tls.plot_tree(DATA, 'results/Tree/titanic_tree.png')
