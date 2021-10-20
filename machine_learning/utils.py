"""
Useful functions to clean up the code for building models
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold

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


def split_in_folds_regression(df: pd.DataFrame, n, target_feature):
    df_sorted = df.sort_values(target_feature)
    full_index_set = set(range(len(df)))
    remaining_index_set = full_index_set.copy()
    random_chance = n
    folds = []
    for _ in range(n):
        remaining_index_list = np.array(list(remaining_index_set))
        randoms = (
            (np.random.uniform(0, random_chance, len(remaining_index_set)) + 1)
            // random_chance
        )
        indexes = remaining_index_list[randoms == 1]
        remaining_index_set.difference_update(set(indexes))
        folds.append(df_sorted.iloc[indexes])
        random_chance -= 1
    return folds


def split_in_folds_classification(df: pd.DataFrame, n, target_feature):
    skf = StratifiedKFold(n, shuffle=True)
    folds = []
    for _, test_indices in skf.split(df, df[target_feature]):
        folds.append(df.iloc[test_indices])
    return folds


def extract_target_feature(df, target_feature):
    target = df[target_feature]
    df = df.drop(columns=[target_feature])
    return df, target


def scale_features(df_train, df_test, features):
    sc = StandardScaler()
    df_train = df_train.copy()
    df_train[features] = sc.fit_transform(df_train[features])
    if df_test is not None:
        df_test = df_test.copy()
        df_test[features] = sc.transform(df_test[features])
    return df_train, df_test


def print_stdout_and_file(string, file_pointer):
    print(string, flush=True)
    print(string, file=file_pointer, flush=True)
