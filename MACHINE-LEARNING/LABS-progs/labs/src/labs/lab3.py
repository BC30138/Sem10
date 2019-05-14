from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.externals.six import StringIO
import pandas as pd
import tools as tls
import pydot



def titanic():
    data = tls.MLStructure()
    train_set = pd.read_csv('data/titanic/train.csv')
    train_set = tls.titanic_preprocessing(train_set)
    data.x_train, data.y_train = tls.titanic_get_train_x_y(train_set)

    x_test_set = pd.read_csv('data/titanic/test.csv')
    y_test_set = pd.read_csv('data/titanic/gender_submission.csv')
    data.x_test = tls.titanic_preprocessing(x_test_set)
    data.y_test = y_test_set['Survived']

    data.clf = DecisionTreeClassifier(max_depth=3, max_leaf_nodes=5) # идеальное дерево 3

    data.classify()
    data.show_stat()

    dot_data = StringIO()
    export_graphviz(data.clf, out_file=dot_data, filled=True, rounded=True,
                special_characters=True)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph[0].write_png('results/Tree/titanic_tree.png')


