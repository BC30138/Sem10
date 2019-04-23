import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

#TODO: x, y in class
class MLStructure(object):
    x = None
    y = None
    clf = None
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    y_result = None

# функция перевода строкового массива элементов выборки в числовой 
def to_numeric(some_fit, ArrayToEncode):
    # инциируем средство для перекодировки строк в численный формат
    le = preprocessing.LabelEncoder()
    le.fit(some_fit)
    numeric_array = []
    for element in ArrayToEncode: 
        numeric_array.append(le.transform(element))
    return np.array(numeric_array)

def read_string_data(some_fit, path):
    return to_numeric(some_fit, np.loadtxt(path, dtype='str', delimiter=',')) 

def get_accuracy_list(data, min_test_ratio, max_test_ratio, step_count):
    step = (max_test_ratio - min_test_ratio) / step_count
    accuracy_list = []
    iterator = min_test_ratio
    while iterator <= max_test_ratio:
        data.x_train, data.x_test, data.y_train, data.y_test =  train_test_split(data.x, data.y, test_size=test_train_ratio)
        data.clf.fit()
        accuracy_list.append([1 - iterator, clf.accuracy])
        iterator += step
        iterator = round(iterator,2)
    return np.array(accuracy_list)

def plot_precision(points, plot_path):
    x, y = points.T
    plt.plot(x, y, marker='o', markerfacecolor='orange', markersize=6, color='skyblue', linewidth=2)
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
    data_frame = input_frame.copy()
    Y = data_frame['Survived'].ravel()
    X = data_frame.drop('Survived', axis=1)
    return X, Y

def show_stat(data):
    print("Size of train: ", len(data.x_train))
    print("Size of test: ", len(data.x_test))
    print("Accuracy: ", accuracy_score(data.y_test, data.y_result))
    print('Confusion matrix: \n', confusion_matrix(data.y_test, data.y_result))



    

