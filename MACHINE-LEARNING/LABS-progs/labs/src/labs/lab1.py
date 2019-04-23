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

    def __init__(self, X, Y):
        # в случае титаника классы определены в другом столбце, поэтому 
        # реализация немного другая
        self.clf = GaussianNB()
        self.X_train = X
        self.Y_train = Y

    def classification(self, test_train_ratio):
        # разбиваем набор данных на обучающую и тестовую выборку
        self.X_train, self.X_test, self.Y_train, self.Y_test =  train_test_split(self.X, self.Y, test_size=test_train_ratio)
        # процесс обучения
        self.clf.fit(self.X_train, self.Y_train)
        # классификация тестовой выборки
        self.Y_result = self.clf.predict(self.X_test)
        self.accuracy = accuracy_score(self.Y_test, self.Y_result)

    def classification(self, X_test, Y_test):
        self.clf.fit(self.X_train, self.Y_train)
        self.Y_result = self.clf.predict(X_test)
        self.accuracy = accuracy_score(Y_test, self.Y_result)
    
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
    n = 50
    X_1 = np.random.normal(10, 4, n)
    X_1 = np.append(X_1, np.random.normal(20, 3, n))
    X_2 = np.random.normal(14, 4, n)
    X_2 = np.append(X_2, np.random.normal(18, 3, n))
    Y = np.full(n, -1)
    Y = np.append(Y, np.ones(n))
    data_set = np.column_stack((X_1, X_2))
    data_set = np.column_stack((data_set, Y))
    tools.plot_data_set(data_set, 'results/NaiveBayes/generated.png')

    test = NaiveBayesLab(data_set)
    accuracy_list = tools.get_accuracy_list(test, 0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/generated_precision.png')

    test.classification(0.2)
    test.show_result()
    print('Confusion matrix: \n', confusion_matrix(test.Y_test, test.Y_result))
    
def titanic():
    cat = preprocessing.OneHotEncoder()
    X_train, Y_train = tools.read_csv_string('data/titanic/train.csv', cat, 1)
    X_test = tools.read_csv_features('data/titanic/test.csv', cat)
    Y_test = tools.read_csv_labels('data/titanic/gender_submission.csv', 'Survived')
    test = NaiveBayesLab(X_train, Y_train)
    test.classification(X_test, Y_test)
    accuracy_list = tools.get_accuracy_list(test, 0.2, 0.9, 10)
    tools.plot_precision(accuracy_list, 'results/NaiveBayes/spam.png')








