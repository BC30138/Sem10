import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
#TODO: переделать X и Y в класс.

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

def read_csv_string(path, cat, class_column):
    data_frame = pd.read_csv(path)
    data_frame = data_frame.fillna(0)
    Y = data_frame.values[:, [class_column]].ravel().astype(int)
    X = np.delete(data_frame.values, class_column, axis=1)
    X = cat.fit_transform(X.astype(str)).toarray()
    return X, Y; 

def read_csv_features(path, cat):
    data_frame = pd.read_csv(path)
    data_frame = data_frame.fillna(0)
    X = cat.transform(data_frame.astype(str)).toarray()
    return X;

def read_csv_labels(path, class_column_name):
    Y = pd.read_csv(path, usecols=[class_column_name], dtype=int)
    return Y; 

def get_accuracy_list(clf, min_test_ratio, max_test_ratio, step_count):
    step = (max_test_ratio - min_test_ratio) / step_count
    accuracy_list = []
    iterator = min_test_ratio
    while iterator <= max_test_ratio:
        clf.classification(iterator)
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

def plot_data_set(data_set, plot_path):
    x, y, c = data_set.T
    plt.scatter(x, y, c=c)
    plt.ylabel('$X_1$')
    plt.xlabel('$X_2$')
    plt.savefig(plot_path)
    plt.close()

