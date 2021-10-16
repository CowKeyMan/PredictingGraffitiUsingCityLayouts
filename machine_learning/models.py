# regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neural_network import MLPRegressor
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.svm import SVR

# classification
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


pow_10_paramter = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]

regression_models = {
    "LinearRegression": {
        "class": LinearRegression,
        "hyperparameters": {},
        "set_parameters": {
            "n_jobs": -1,
        }
    },
    "Ridge": {
        "class": Ridge,
        "hyperparameters": {
            "alpha": pow_10_paramter,
            "tol": pow_10_paramter,
            "solver": [
                "auto",
                "svd",
                "cholesky",
                "lsqr",
                "sparse_cg",
                "sag",
                "saga",
            ]
        },
        "set_parameters": {}
    },
    "Lasso": {
        "class": Lasso,
        "hyperparameters": {
            "alpha": pow_10_paramter,
        },
        "set_parameters": {
            "tol": 0.0001,
            "max_iter": 10000
        }
    },
    # "SVR": {
    #     "class": SVR,
    #     "hyperparameters": {
    #         "degree": list(range(1, 6, 1)),
    #         "tol": pow_10_paramter,
    #         "C": pow_10_paramter,
    #         "epsilon": pow_10_paramter,
    #         "kernel": ["linear", "poly", "rbf", "sigmoid"],
    #     },
    #     "set_parameters": {}
    # },
    # "DecisionTreeRegressor": {
    #     "class": DecisionTreeRegressor,
    #     "hyperparameters": {
    #         "criterion": [
    #             "squared_error",
    #             "friedman_mse",
    #             "absolute_error",
    #         ],
    #         "max_depth": list(range(5, 300, 5)),
    #     },
    #     "set_parameters": {}
    # },
    "MLPRegressor": {
        "class": MLPRegressor,
        "hyperparameters": {
            "hidden_layer_sizes": [
                (200, 200), (100, 100), (100, 100, 100), (200, 100, 100)
            ],
            "activation": ["identity", "logistic", "tanh", "relu"],
            "solver": ["lbfgs", "sgd", "adam"],
            "alpha": pow_10_paramter,
        },
        "set_parameters": {
            "early_stopping": True,
            "max_iter": 500,
        }
    }
}

classification_models = {
    "LogisticRegression": {
        "class": LogisticRegression,
        "hyperparameters": {
            "C": pow_10_paramter,
        },
        "set_parameters": {
            "n_jobs": -1,
            "max_iter": 200
        }
    },
    "BalancedLogisticRegression": {
        "class": LogisticRegression,
        "hyperparameters": {
            "C": pow_10_paramter,
        },
        "set_parameters": {
            "n_jobs": -1,
            "max_iter": 200,
            "class_weight": "balanced"
        }
    },
    # "SVM": {
    #     "class": SVC,
    #     "hyperparameters": {
    #         "C": pow_10_paramter,
    #         "kernel": ["linear", "poly", "rbf", "sigmoid"],
    #         "degree": list(range(1, 6, 1)),
    #     },
    #     "set_parameters": {}
    # },
    # "BalancedSVM": {
    #     "class": SVC,
    #     "hyperparameters": {
    #         "C": pow_10_paramter,
    #         "kernel": ["linear", "poly", "rbf", "sigmoid"],
    #         "degree": list(range(1, 3, 1)),
    #     },
    #     "set_parameters": {
    #         "class_weight": "balanced"
    #     }
    # },
    "MLPClassifier": {
        "class": MLPClassifier,
        "hyperparameters": {
            "hidden_layer_sizes": [
                (200, 200), (100, 100), (100, 100, 100), (200, 100, 100)
            ],
            "activation": ["identity", "logistic", "tanh", "relu"],
            "solver": ["lbfgs", "sgd", "adam"],
            "alpha": pow_10_paramter,
        },
        "set_parameters": {
            "early_stopping": True,
            "max_iter": 500,
        }
    }
}
