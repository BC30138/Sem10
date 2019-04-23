import tools
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

class NaiveBayesLab:
    """Lab 1"""
    def __init__(self, data_set):
        # инициируем классификатор
        self.clf = GaussianNB()
        # инициализируем множество элементов
        self.X = data_set[:, range(len(data_set[0]) - 1)]
        # инициализируем множество классов
        self.Y = data_set[:, [-1]].ravel()

    def classification(self, test_train_ratio):
        # разбиваем набор данных на обучающую и тестовую выборку
        self.X_train, self.X_test, self.Y_train, self.Y_test =  train_test_split(self.X, self.Y, test_size=test_train_ratio)
        # процесс обучения
        self.clf.fit(self.X_train, self.Y_train)
        # классификация тестовой выборки
        self.Y_result = self.clf.predict(self.X_test)
        self.accuracy = accuracy_score(self.Y_test, self.Y_result)
    
    def show_result(self):
        print("Size of train: ", len(self.X_train))
        print("Size of test: ", len(self.X_test))
        print("Accuracy: ", self.accuracy)


def tic_tac_toe():
    print("Tic_tac_toe.txt")
    # задаем строки-образцы для перекодировки
    tic_tac_fit = ['x', 'o', 'b', 'positive','negative']
    # чтение выборки данных
    data_set = tools.read_string_data(tic_tac_fit, 'data/Tic_tac_toe.txt')
    test = NaiveBayesLab(data_set)
    accuracy_list = tools.get_accuracy_list(test, 0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/tic_tac_toe.png')


def spam():
    print("Spambase.data")
    data_set = np.loadtxt('data/spambase.data', delimiter=',')
    test = NaiveBayesLab(data_set)
    accuracy_list = tools.get_accuracy_list(test, 0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/spam.png')

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

    x = data_frame.drop('Y', axis=1)
    y = data_frame['Y'].ravel()

    data.clf = GaussianNB()
    accuracy_list = tools.get_accuracy_list(data, 0.2, 0.9, 10)
    # tools.plot_precision(accuracy_list, 'results/NaiveBayes/generated_precision.png')

    # test.classification(0.2)
    # test.show_result()
    # print('Confusion matrix: \n', confusion_matrix(test.Y_test, test.Y_result))
    
def titanic():
    data = tools.MLStructure()
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tools.titanic_preprocessing(train_set)
    data.x_train, data.y_train = tools.titanic_get_train_X_Y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    data.x_test = tools.titanic_preprocessing(x_test_set)
    data.y_test = y_test_set['Survived'].ravel()

    clf = GaussianNB()
    clf.fit(data.x_train, data.y_train)
    data.y_result = clf.predict(data.x_test)
    tools.show_stat(data)
    
def titanic_split():
    data = tools.MLStructure()
    data_frame = pd.read_csv('data/titanic/train.csv')
    data_frame = tools.titanic_preprocessing(data_frame)
    x, y = tools.titanic_get_train_X_Y(data_frame)
    data.x_train, data.x_test, data.y_train, data.y_test =  train_test_split(x, y, test_size=0.1)
    
    clf = GaussianNB()
    clf.fit(data.x_train, data.y_train)
    data.y_result = clf.predict(data.x_test)
    tools.show_stat(data)





