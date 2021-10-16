from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor

pow_10_paramter = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]

regression_models = {
    "LinearRegression": {
        "class": LinearRegression,
        "hyperparameters": {},
        "set_parameters": {
            "n_jobs": -1
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
                "lbfgs"
            ]
        },
        "set_parameters": {}
    },
    "Lasso": {
        "class": Lasso,
        "hyperparameters": {
            "alpha": pow_10_paramter,
            "tol": pow_10_paramter,
        },
        "set_parameters": {}
    },
    "ElasticNet": {
        "class": ElasticNet,
        "hyperparameters": {
            "alpha": pow_10_paramter,
            "tol": pow_10_paramter,
        },
        "set_parameters": {}
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
    #             "mse",
    #             "friedman_mse",
    #             "absolute_error",
    #             "mae",
    #             "poisson"
    #         ],
    #         "max_depth": list(range(5, 100, 5)),
    #         "tol": pow_10_paramter,
    #         "C": pow_10_paramter,
    #         "epsilon": pow_10_paramter,
    #         "kernel": ["linear", "poly", "rbf", "sigmoid"],
    #     },
    #     "set_parameters": {}
    # },
    # "MLPRegressor": {
    #     "class": MLPRegressor,
    #     "hyperparameters": {},
    #     "set_parameters": {}
    # }
}
