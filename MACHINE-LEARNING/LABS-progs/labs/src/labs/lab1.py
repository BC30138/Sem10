import tools
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB

def tic_tac_toe():
    data = tools.MLStructure()
    data_frame = pd.read_csv('data/Tic_tac_toe.txt', header=None)
    data.x, data.y = tools.tic_tac_toe_prep_get_X_Y(data_frame)

    data.clf = GaussianNB()
    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/tic_tac_toe.png')
    
    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()

def spam():
    data = tools.MLStructure()
    data_frame = pd.read_csv('data/spambase.data', header=None)
    data.x, data.y = tools.spam_get_X_Y(data_frame)

    data.clf = GaussianNB()

    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/spam.png')
    
    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()

def generate_points():
    data = tools.MLStructure()
    data_frame = pd.DataFrame()

    n = 50
    X_1 = np.random.normal(10, 4, n)
    X_1 = np.append(X_1, np.random.normal(20, 3, n))
    X_2 = np.random.normal(14, 4, n)
    X_2 = np.append(X_2, np.random.normal(18, 3, n))
    Y = np.full(n, -1)
    Y = np.append(Y, np.ones(n))

    data_frame['X_1'] = X_1
    data_frame['X_2'] = X_2
    data_frame['Y'] = Y
    tools.plot_data_set(data_frame, 'X_1', 'X_2', 'Y', 'results/NaiveBayes/generated.png')

    data.x = data_frame.drop('Y', axis=1)
    data.y = data_frame['Y']

    data.clf = GaussianNB()

    accuracy_list = data.get_accuracy_volume_dependency(0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/generated_precision.png')

    data.split_data_into_test_train(0.2)
    data.classify()
    data.show_stat()
    
def titanic():
    data = tools.MLStructure()
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tools.titanic_preprocessing(train_set)
    data.x_train, data.y_train = tools.titanic_get_train_X_Y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    data.x_test = tools.titanic_preprocessing(x_test_set)
    data.y_test = y_test_set['Survived']

    data.clf = GaussianNB()

    data.classify()
    data.show_stat()
    
def titanic_split():
    data = tools.MLStructure()
    data_frame = pd.read_csv('data/titanic/train.csv')
    data_frame = tools.titanic_preprocessing(data_frame)
    data.x, data.y = tools.titanic_get_train_X_Y(data_frame)

    data.clf = GaussianNB()

    data.split_data_into_test_train(0.1)
    data.classify()
    data.show_stat()
