"""
Useful functions to clean up the code for building models
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold


def split_in_folds(df: pd.DataFrame, n, target_feature):
    skf = StratifiedKFold(n, shuffle=True)
    folds = []
    for _, test_indices in skf.split(df, df[target_feature]):
        folds.append(df.iloc[test_indices])
    return folds


def extract_target_feature(df, target_feature):
    target = df[target_feature]
    df = df.drop(columns=[target_feature])
    return df, target


def regularize_features(df_train, df_test, features):
    sc = StandardScaler()
    df_train = df_train.copy()
    df_test = df_test.copy()
    df_train[features] = sc.fit_transform(df_train[features])
    df_test[features] = sc.transform(df_test[features])
    return df_train, df_test
