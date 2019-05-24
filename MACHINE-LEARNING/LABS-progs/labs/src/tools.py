"""Usefull common tools for labs"""
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.metrics.pairwise import polynomial_kernel
import pydotplus as pdot

class MLStructure(object):
    """Class, which contains all necessary data for data-analysis"""
    x = None
    y = None
    clf = None
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    y_result = None

    def split_data_into_test_train(self, test_ratio):
        """Split data-set to test and train wth ration"""
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=test_ratio)

    def get_accuracy_volume_dependency(self, min_test_ratio, max_test_ratio, step_count):
        """Method returns array with relative volume of train set and accuracy for it"""
        step = (max_test_ratio - min_test_ratio) / step_count
        accuracy_list = []
        test_ratio = min_test_ratio
        while test_ratio <= max_test_ratio:
            acc_sum = 0
            self.split_data_into_test_train(test_ratio)
            for it in range(5):
                self.classify()
                acc_sum += accuracy_score(self.y_test, self.y_result)
            accuracy_list.append([1 - test_ratio, acc_sum / 5])
            test_ratio += step
            test_ratio = round(test_ratio, 2)
        return np.array(accuracy_list)

    def classify(self):
        """Run classification process"""
        self.clf.fit(self.x_train, self.y_train)
        self.y_result = self.clf.predict(self.x_test)

    def my_distance(self, weights):
        # kde = KernelDensity(kernel="epanechnikov").fit(self.x_train[0])
        # print(len(self.x_train.index))
        # result = kde.score_samples(weights[0])
        result = polynomial_kernel(weights)
        print(result)
        return result

    def show_stat(self):
        """Show necessary ML stats"""
        print("Size of train: ", len(self.x_train))
        print("Size of test: ", len(self.x_test))
        print("Accuracy: ", accuracy_score(self.y_test, self.y_result))
        print('Confusion matrix: \n', confusion_matrix(self.y_test, self.y_result))

def plot_precision(accuracy_list, plot_path):
    """Plot 2D schedule with accuracy and relative volume of train set"""
    test_ratio, accuracy = accuracy_list.T
    plt.plot(test_ratio, accuracy, marker='o', markerfacecolor='orange', markersize=6, color='skyblue', linewidth=2)
    plt.ylabel('Accuracy score')
    plt.xlabel('Relative volume of trainig sample')
    plt.savefig(plot_path)
    plt.close()

def plot_tree_precision(accuracy_list, plot_path):
    """Plot 2D schedule with accuracy and number of leafes"""
    leaf_num, accuracy = accuracy_list.T
    plt.plot(leaf_num, accuracy, marker='o', markerfacecolor='orange', markersize=6, color='skyblue', linewidth=2)
    plt.ylabel('Accuracy score')
    plt.xlabel('Max leaf nodes')
    plt.savefig(plot_path)
    plt.close()

def plot_data_set(data_set, column_x_1, column_x_2, column_class, plot_path):
    """Plot 2D schedule of data-set, which contains two classes only"""
    x_1 = data_set[column_x_1].ravel()
    x_2 = data_set[column_x_2].ravel()
    bin_c = data_set[column_class].ravel()
    plt.scatter(x_1, x_2, c=bin_c)
    plt.ylabel('$X_1$')
    plt.xlabel('$X_2$')
    plt.savefig(plot_path)
    plt.close()

def titanic_preprocessing(input_frame):
    """Preprocessing for titanic data-set"""
    data_frame = input_frame.copy()
    data_frame['Name'] = data_frame['Name'].apply(len)
    data_frame['Sex'] = data_frame['Sex'].map({'male': 0, 'female': 1}).astype(int)
    data_frame['Age'] = data_frame['Age'].fillna(data_frame['Age'].mean(skipna=True)).astype(int)
    data_frame['FamilySize'] = data_frame['SibSp'] + data_frame['Parch'] + 1
    data_frame['HasCabin'] = data_frame['Cabin'].apply(lambda x: 0 if isinstance(x, float) else 1)
    data_frame['Fare'] = data_frame['Fare'].fillna(data_frame['Fare'].mean(skipna=True)).astype(int)
    data_frame['Embarked'] = data_frame['Embarked'].fillna('S').map({'S': 0, 'C': 1, 'Q': 2}).astype(int)

    data_frame = data_frame.drop(['PassengerId', 'SibSp', 'Parch', 'Ticket', 'Cabin'], axis=1)
    return data_frame

def titanic_get_train_x_y(input_frame):
    """Split data-set 'titanic' to X-mantrix and Y-array"""
    y_arr = input_frame['Survived']
    x_tab = input_frame.drop('Survived', axis=1)
    return x_tab, y_arr

def spam_get_x_y(input_frame):
    """Split data-set 'spam' to X-mantrix and Y-array"""
    y_arr = input_frame[input_frame.columns[len(input_frame.columns) - 1]]
    x_tab = input_frame.drop(input_frame.columns[len(input_frame.columns) - 1], axis=1)
    return x_tab, y_arr

def tic_tac_toe_prep_get_x_y(input_frame):
    """Preprocess and split data-set 'tic-tac-toe' to X-mantrix and Y-array"""
    y_arr = input_frame[input_frame.columns[len(input_frame.columns) - 1]]
    x_tab = input_frame.drop(input_frame.columns[len(input_frame.columns) - 1], axis=1)
    x_tab = x_tab.replace({'x': 0, 'o': 1, 'b': 2}).astype(int)
    y_arr = y_arr.map({'positive': 0, 'negative': 1}).astype(int)
    return x_tab, y_arr

def plot_tree(ml_struct, output_filename):
    """Plot result tree"""
    dot_data = StringIO()
    classes = list(map(str, ml_struct.clf.classes_))
    export_graphviz(ml_struct.clf, out_file=dot_data, filled=True, rounded=True,
                    special_characters=True, class_names=classes, feature_names=list(ml_struct.x_train))
    graph = pdot.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(output_filename)

def plot_tree_rotate(ml_struct, output_filename):
    """Plot result tree"""
    dot_data = StringIO()
    classes = list(map(str, ml_struct.clf.classes_))
    export_graphviz(ml_struct.clf, out_file=dot_data, filled=True, rounded=True,
                    special_characters=True, class_names=classes, feature_names=list(ml_struct.x_train), rotate=True)
    graph = pdot.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(output_filename)

def plot_tree_no_predict(ml_struct, output_filename):
    """Plot result tree"""
    dot_data = StringIO()
    classes = list(map(str, ml_struct.clf.classes_))
    export_graphviz(ml_struct.clf, out_file=dot_data, filled=True, rounded=True,
                    special_characters=True, class_names=classes, feature_names=list(ml_struct.x))
    graph = pdot.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(output_filename)

def plot_tree_regr(ml_struct, output_filename):
    """Plot result tree"""
    dot_data = StringIO()
    # classes = list(map(str, ml_struct.clf.classes_))
    export_graphviz(ml_struct.clf, out_file=dot_data, filled=True, rounded=True,
                    special_characters=True, feature_names=list(ml_struct.x))
    graph = pdot.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(output_filename)

def glass_get_x_y(input_frame):
    """Split data-set 'glass' to X-mantrix and Y-array"""
    y_arr = input_frame[10]
    x_tab = input_frame.drop([0,10], axis=1)
    x_tab.columns = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe"]
    return x_tab, y_arr

def spam7_get_x_y(input_frame):
    """Split data-set 'spam7' to X-mantrix and Y-array"""
    y_arr = input_frame['yesno'].map({'y': 1, 'n': 0}).astype(int)
    x_tab = input_frame.drop('yesno', axis=1)
    return x_tab, y_arr

def nsw74psid1_get_x_y(input_frame):
    """Split data-set 'nsw74psid1' to X-mantrix and Y-array"""
    y_arr = input_frame['re78']
    x_tab = input_frame.drop('re78', axis=1)
    return x_tab, y_arr

def lenses_get_x_y(input_frame):
    """Split data-set 'lenses' to X-mantrix and Y-array"""
    y_arr = input_frame['Type']
    x_tab = input_frame.drop(['Id','Type'], axis=1)
    return x_tab, y_arr

def svmdata_get_x_y(input_frame):
    """Split data-set 'svmdata' to X-mantrix and Y-array"""
    y_arr = input_frame['Colors'].map({'green': 1, 'red': 0}).astype(int)
    x_tab = input_frame.drop('Colors', axis=1)
    return x_tab, y_arr
