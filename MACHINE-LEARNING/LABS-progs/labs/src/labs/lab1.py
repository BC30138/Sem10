"""lab1: Naive Bayes"""
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import tools as tls

def tic_tac_toe():
    """'Tic-tac-toe' data-set"""
    data = tls.MLStructure()
    data_frame = pd.read_csv('data/Tic_tac_toe.txt', header=None)
    data.x, data.y = tls.tic_tac_toe_prep_get_x_y(data_frame)

    data.clf = GaussianNB()
    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tls.plot_precision(accuracy_list, 'results/NaiveBayes/tic_tac_toe.png')

    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()

def spam():
    """'Spam' data-set"""
    data = tls.MLStructure()
    data_frame = pd.read_csv('data/spambase.data', header=None)
    data.x, data.y = tls.spam_get_x_y(data_frame)

    data.clf = GaussianNB()

    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tls.plot_precision(accuracy_list, 'results/NaiveBayes/spam.png')

    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()

def generate_points():
    """Generated data-set"""
    data = tls.MLStructure()
    data_frame = pd.DataFrame()

    class_size = 50
    x_1 = np.random.normal(10, 4, class_size)
    x_1 = np.append(x_1, np.random.normal(20, 3, class_size))
    x_2 = np.random.normal(14, 4, class_size)
    x_2 = np.append(x_2, np.random.normal(18, 3, class_size))
    y_arr = np.full(class_size, -1)
    y_arr = np.append(y_arr, np.ones(class_size))

    data_frame['X_1'] = x_1
    data_frame['X_2'] = x_2
    data_frame['Y'] = y_arr
    tls.plot_data_set(data_frame, 'X_1', 'X_2', 'Y', 'results/NaiveBayes/generated.png')

    data.x = data_frame.drop('Y', axis=1)
    data.y = data_frame['Y']

    data.clf = GaussianNB()

    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tls.plot_precision(accuracy_list, 'results/NaiveBayes/generated_precision.png')

    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()

def titanic():
    """'Titanic' data-set with given data-set for testing"""
    data = tls.MLStructure()
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tls.titanic_preprocessing(train_set)
    data.x_train, data.y_train = tls.titanic_get_train_x_y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    data.x_test = tls.titanic_preprocessing(x_test_set)
    data.y_test = y_test_set['Survived']

    data.clf = GaussianNB()

    data.classify()
    data.show_stat()

def titanic_split():
    """'Titanic' data-set with spliting data-set to train and test"""
    data = tls.MLStructure()
    data_frame = pd.read_csv('data/titanic/train.csv')
    data_frame = tls.titanic_preprocessing(data_frame)
    data.x, data.y = tls.titanic_get_train_x_y(data_frame)

    data.clf = GaussianNB()

    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tls.plot_precision(accuracy_list, 'results/NaiveBayes/titanic.png')

    data.split_data_into_test_train(0.1)
    data.classify()
    data.show_stat()
