"""
Useful functions to clean up the code for building models
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler


def split_in_folds(df: pd.DataFrame, n):
    df = df.sample(frac=1, ignore_index=True)
    folds = []
    fold_size = len(df) / n
    for i in range(n):
        folds.append(df.iloc[round(fold_size * i): round(fold_size * (i + 1))])
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
