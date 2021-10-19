"""
Use the buildings_model_features csv to build models using sklearn

Here we do cross validation and hyperparameter tuning for each
model that we train, using sklearn
"""

import warnings

from models import regression_models as models
from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
import numpy as np
from utils import (
    split_in_folds_regression,
    extract_target_feature,
    regularize_features,
    print_stdout_and_file,
)
np.random.seed(42)
from sklearn.exceptions import ConvergenceWarning

file_pointer \
    = open('resources/machine_learning_results/regression_models.txt', 'w')

fold_amount = 5
continuous_variables = [
    'highest_elevation_m',
    'area_m2',
    'sub_buildings',
    'geo_local_area_area_m2',
    'geo_local_area_population',
    'pop_density',
]
for name in ['one_house_away', 'two_houses_away', 'four_houses_away']:
    continuous_variables += [
        f'{name}_buildings_count',
        f'{name}_graffiti_count',
        f'{name}_graffiti_average',
        f'{name}_graffiti_buildings',
        f'{name}_buildings_average_height',
        f'{name}_buildings_median_height',
        f'{name}_buildings_total_sub_buildings',
        f'{name}_buildings_average_sub_buildings',
        f'{name}_buildings_median_sub_buildings',
        f'{name}_street_lights',
    ]

target_value = 'graffiti_count'

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')

for name, model in models.items():
    print_stdout_and_file(f'Now training {name}', file_pointer)
    # Hyper parameter tuning on subset of the dataset
    folds = split_in_folds_regression(df, len(df) // 5000, target_value)
    df_tuning_full = folds[0]  # 5000 exmamples

    print('\tTuning...')
    tuner = RandomizedSearchCV(
        model['class'](**model['set_parameters']),
        model['hyperparameters'],
        refit=False,
        n_iter=20,
    )
    df_tuning_full, _ \
        = regularize_features(df_tuning_full, None, continuous_variables)
    df_tuning, y_tuning = extract_target_feature(df_tuning_full, target_value)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        tuner.fit(df_tuning.values, y_tuning.values)
    best_params = tuner.best_params_ | model['set_parameters']
    print_stdout_and_file(f'\t\tBest Params: {best_params}', file_pointer)

    # k-fold validation
    folds = split_in_folds_regression(df, fold_amount, target_value)
    for i in range(fold_amount):
        df_test = folds[i]
        df_train = pd.concat(folds[0:i] + folds[i + 1:fold_amount])
        df_test, y_test = extract_target_feature(df_test, target_value)
        df_train, y_train = extract_target_feature(df_train, target_value)

        df_train, df_test \
            = regularize_features(df_train, df_test, continuous_variables)

        regressor = model['class'](**best_params)
        print_stdout_and_file(
            f'\t\tFitting fold {i+1}/{fold_amount}', file_pointer
        )
        regressor.fit(df_train.values, y_train.values)
        print_stdout_and_file(
            '\t\t\tr^2 on train: '
            f'{regressor.score(df_train.values, y_train.values)}',
            file_pointer
        )
        print_stdout_and_file(
            '\t\t\tr^2 on test: '
            f'{regressor.score(df_test.values, y_test.values)}',
            file_pointer
        )
        df_test_not_0 = df_test[y_test > 0]
        y_test_not_0 = y_test[y_test > 0]
        print_stdout_and_file(
            '\t\t\tr^2 on test not 0: '
            f'{regressor.score(df_test_not_0.values, y_test_not_0.values)}',
            file_pointer
        )
        print_stdout_and_file("", file_pointer)

file_pointer.close()
