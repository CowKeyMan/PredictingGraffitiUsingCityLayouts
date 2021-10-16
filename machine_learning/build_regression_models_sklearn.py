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
from utils import \
    split_in_folds_regression, extract_target_feature, regularize_features
np.random.seed(42)
# warnings.simplefilter("ignore")


fold_amount = 5
continuous_variables = [
    'highest_elevation_m',
    'area_m2',
    'sub_buildings',
    'nearby_buildings_count',
    'nearby_graffiti_count',
    'nearby_graffiti_average',
    'nearby_graffiti_buildings',
    'nearby_buildings_average_height',
    'nearby_buildings_median_height',
    'nearby_buildings_total_sub_buildings',
    'nearby_buildings_average_sub_buildings',
    'nearby_buildings_median_sub_buildings',
    'nearby_street_lights',
    'geo_local_area_area_m2',
    'geo_local_area_population',
    'pop_density',
]
target_value = 'graffiti_count'


df = pd.read_csv('resources/data/generated/buildings_model_features.csv')

for name, model in models.items():
    print(f'Now training {name}')
    # Hyper parameter tuning on subset of the dataset
    folds = split_in_folds_regression(df, len(df) // 5000, target_value)
    df_tuning_full = pd.concat(folds[:1])  # 5000 exmamples

    print('\tTuning...')
    tuner = RandomizedSearchCV(
        model['class'](**model['set_parameters']),
        model['hyperparameters'],
        n_jobs=-1,
        refit=False
    )
    df_tuning_full, _ \
        = regularize_features(df_tuning_full, None, continuous_variables)
    df_tuning, y_tuning = extract_target_feature(df_tuning_full, target_value)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        tuner.fit(df_tuning, y_tuning)
    best_params = tuner.best_params_ | model['set_parameters']
    print(f'\t\tBest Params: {best_params}')

    # k-fold validation
    folds = split_in_folds_regression(df, fold_amount, target_value)
    for i in range(fold_amount):
        df_test = folds[i]
        df_train = pd.concat(folds[0:i] + folds[i + 1:fold_amount])
        df_test, y_test = extract_target_feature(df_test, target_value)
        df_train, y_train = extract_target_feature(df_train, target_value)

        print(df_train.columns)
        print(y_test)

        df_train, df_test \
            = regularize_features(df_train, df_test, continuous_variables)

        regressor = model['class'](**best_params)
        print(f'\t\tFitting fold {i+1}/{fold_amount}')
        regressor.fit(df_train, y_train)
        print(f'\t\t\tr^2 on train: {regressor.score(df_train, y_train)}')
        print(f'\t\t\tr^2 on test: {regressor.score(df_test, y_test)}')
        df_test_not_0 = df_test[y_test > 0]
        y_test_not_0 = y_test[y_test > 0]
        print(
            '\t\t\tr^2 on test not 0: '
            f'{regressor.score(df_test_not_0, y_test_not_0)}'
        )
        print()
