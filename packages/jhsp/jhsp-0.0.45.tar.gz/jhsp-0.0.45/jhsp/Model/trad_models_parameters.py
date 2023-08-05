import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


def GetTraMandP(model_name):


    # 模型定义
    RF_parameters = {
        'n_estimators': range(20, 800, 10),
        'criterion': ['entropy', 'gini'],
        'max_depth': range(5, 25, 1),
        'max_features': ['auto', 'sqrt', 'log2'],
        'min_samples_split': range(2, 5, 1),
    }

    KNN_parameters = {
        'n_neighbors': range(1, 10, 1),
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
    }

    SVC_parameters = {
        'C': np.arange(1, 8, 0.2),
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        'gamma': ['scale', 'auto'],
        'degree': range(1, 11, 1)
    }

    # 模型列表
    models_dict = {'RF': RandomForestClassifier(),
                   'KNN': KNeighborsClassifier(),
                   'SVC': SVC()}

    # 模型参数字典
    param_dict = {'RF': RF_parameters,
                      'KNN': KNN_parameters,
                      'SVC': SVC_parameters}

    return models_dict[model_name],param_dict[model_name]

