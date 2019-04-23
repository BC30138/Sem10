import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class MLStructure(object):
    x = None 
    y = None 
    clf = None
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    y_result = None

    def split_data_into_test_train(self, test_ratio):
        self.x_train, self.x_test, self.y_train, self.y_test =  train_test_split(self.x, self.y, test_size=test_ratio)

    def get_accuracy_volume_dependency(self, min_test_ratio, max_test_ratio, step_count):
        step = (max_test_ratio - min_test_ratio) / step_count
        accuracy_list = []
        test_ratio = min_test_ratio
        while test_ratio <= max_test_ratio:
            self.split_data_into_test_train(test_ratio)
            self.classify()
            accuracy_list.append([1 - test_ratio, accuracy_score(self.y_test, self.y_result)])
            test_ratio += step
            test_ratio = round(test_ratio,2)
        return np.array(accuracy_list)

    def classify(self):
        self.clf.fit(self.x_train, self.y_train)
        self.y_result = self.clf.predict(self.x_test)
    
    def show_stat(self):
        print("Size of train: ", len(self.x_train))
        print("Size of test: ", len(self.x_test))
        print("Accuracy: ", accuracy_score(self.y_test, self.y_result))
        print('Confusion matrix: \n', confusion_matrix(self.y_test, self.y_result))

def plot_precision(accuracy_list, plot_path):
    test_ratio, accuracy = accuracy_list.T
    plt.plot(test_ratio, accuracy, marker='o', markerfacecolor='orange', markersize=6, color='skyblue', linewidth=2)
    plt.ylabel('Accuracy score')
    plt.xlabel('Relative volume of trainig sample')
    plt.savefig(plot_path)
    plt.close()

def plot_data_set(data_set, column_x_1, column_x_2, column_class, plot_path):
    x_1 = data_set[column_x_1].ravel()
    x_2 = data_set[column_x_2].ravel()
    c = data_set[column_class].ravel()
    plt.scatter(x_1, x_2, c=c)
    plt.ylabel('$X_1$')
    plt.xlabel('$X_2$')
    plt.savefig(plot_path)
    plt.close()

def titanic_preprocessing(input_frame):
    data_frame = input_frame.copy()
    data_frame['Name'] = data_frame['Name'].apply(len)
    data_frame['Sex'] = data_frame['Sex'].map({'male': 0, 'female': 1}).astype(int)
    data_frame['Age'] = data_frame['Age'].fillna(data_frame['Age'].mean(skipna=True)).astype(int)
    data_frame['FamilySize'] = data_frame['SibSp'] + data_frame['Parch'] + 1
    data_frame['HasCabin'] = data_frame['Cabin'].apply(lambda x: 0 if type(x) == float else 1)
    data_frame['Fare'] = data_frame['Fare'].fillna(data_frame['Fare'].mean(skipna=True)).astype(int)
    data_frame['Embarked'] = data_frame['Embarked'].fillna('S').map({'S': 0, 'C': 1, 'Q': 2}).astype(int)

    data_frame = data_frame.drop(['PassengerId','SibSp', 'Parch', 'Ticket', 'Cabin'], axis=1)
    return data_frame

def titanic_get_train_X_Y(input_frame):
    y = input_frame['Survived']
    x = input_frame.drop('Survived', axis=1)
    return x, y

def spam_get_X_Y(input_frame):
    y = input_frame[input_frame.columns[len(input_frame.columns) - 1]]
    x = input_frame.drop(input_frame.columns[len(input_frame.columns) - 1], axis=1)
    return x, y

def tic_tac_toe_prep_get_X_Y(input_frame):
    y = input_frame[input_frame.columns[len(input_frame.columns) - 1]]
    x = input_frame.drop(input_frame.columns[len(input_frame.columns) - 1], axis=1)
    x = x.replace({'x': 0, 'o': 1, 'b': 2}).astype(int)
    y = y.map({'positive': 0,'negative': 1}).astype(int)
    return x, y





    

