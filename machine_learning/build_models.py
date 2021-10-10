"""
Use the buildings_model_features csv to build a model

Here we do cross validation and hyperparameter tuning for each
model that we train, using sklearn
"""

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import pandas as pd
import numpy as np
from utils import split_in_folds, extract_target_feature, regularize_features
np.random.seed(42)


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


df = pd.read_csv('resources/data/generated/buildings_model_features.csv')

folds = split_in_folds(df, fold_amount)

for i in range(fold_amount):
    df_test = folds[i]
    df_train = pd.concat(folds[0:i] + folds[i + 1:fold_amount])
    df_test, y_test = extract_target_feature(df_test, 'graffiti_count')
    df_train, y_train = extract_target_feature(df_train, 'graffiti_count')

    df_train, df_test \
        = regularize_features(df_train, df_test, continuous_variables)

    # TODO: do hyper parameter tuning on subset of the dataset here

    model = LinearRegression()
    # model = SVR(verbose=True)
    model.fit(df_train, y_train)
    print(f'fold {i + 1}')
    print(f'r^2 on train: {model.score(df_train, y_train)}')
    print(f'r^2 on test: {model.score(df_test, y_test)}')
    df_test_not_0 = df_test[y_test > 0]
    y_test_not_0 = y_test[y_test > 0]
    print(f'r^2 on test not 0: {model.score(df_test_not_0, y_test_not_0)}')
    print()
