"""
Use the buildings_model_features csv to build models using sklearn

Here we do cross validation and hyperparameter tuning for each
model that we train, using sklearn
"""

import warnings

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from models import classification_models as models
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import \
    accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import pandas as pd
import numpy as np
from utils import (
    split_in_folds_classification,
    extract_target_feature,
    regularize_features,
    print_stdout_and_file,
)
np.random.seed(42)
from sklearn.exceptions import ConvergenceWarning


def plot_confusion_matrix(confusion_matrix, labels, fig_name):
    cm = confusion_matrix
    cmap = LinearSegmentedColormap.from_list("", ["white", "darkBlue"])
    sns.heatmap(
        cm, annot=True, xticklabels=labels, yticklabels=labels, cmap=cmap, vmin=0, fmt="d"
    )
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.rcParams["figure.figsize"] = [15, 9]
    plt.savefig(f'resources/machine_learning_results/{fig_name}')
    plt.clf()


file_pointer \
    = open('resources/machine_learning_results/classification_models.txt', 'w')

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
target_value = 'has_graffiti'

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
df['has_graffiti'] = (df['graffiti_count'] > 0).astype(float)
df.drop(columns='graffiti_count', inplace=True)

for name, model in models.items():
    print_stdout_and_file(f'Now training {name}', file_pointer)
    # Hyper parameter tuning on subset of the dataset
    folds = split_in_folds_classification(df, len(df) // 10000, target_value)
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
    folds = split_in_folds_classification(df, fold_amount, target_value)
    confusion_matrices = []
    for i in range(fold_amount):
        df_test = folds[i]
        df_train = pd.concat(folds[0:i] + folds[i + 1:fold_amount])
        df_test, y_test = extract_target_feature(df_test, target_value)
        df_train, y_train = extract_target_feature(df_train, target_value)

        df_train, df_test \
            = regularize_features(df_train, df_test, continuous_variables)

        classifier = model['class'](**best_params)
        print_stdout_and_file(
            f'\t\tFitting fold {i+1}/{fold_amount}', file_pointer
        )
        classifier.fit(df_train.values, y_train.values)
        train_predictions = classifier.predict(df_train.values)
        print_stdout_and_file(
            '\t\t\taccuracy on train: '
            f'{accuracy_score(y_train.values, train_predictions)}',
            file_pointer
        )
        print_stdout_and_file(
            '\t\t\tf1 on train: '
            f'{f1_score(y_train.values, train_predictions)}',
            file_pointer
        )
        test_predictions = classifier.predict(df_test.values)
        print_stdout_and_file(
            '\t\t\taccuracy on test: '
            f'{accuracy_score(y_test.values, test_predictions)}',
            file_pointer
        )
        print_stdout_and_file(
            '\t\t\tprecision on test: '
            f'{precision_score(y_test.values, test_predictions)}',
            file_pointer
        )
        print_stdout_and_file(
            '\t\t\trecall on test: '
            f'{recall_score(y_test.values, test_predictions)}',
            file_pointer
        )
        print_stdout_and_file(
            '\t\t\tf1 on test: '
            f'{f1_score(y_test.values, test_predictions)}',
            file_pointer
        )
        confusion_matrices.append(
            confusion_matrix(y_test.values, test_predictions)
        )
        print_stdout_and_file("", file_pointer)

    total_confusion_matrix = confusion_matrices[0]
    for cm in confusion_matrices[1:]:
        total_confusion_matrix += cm
    total_confusion_matrix = total_confusion_matrix.astype(float)
    total_confusion_matrix /= len(confusion_matrices)
    total_confusion_matrix = np.round(total_confusion_matrix)
    plot_confusion_matrix(
        cm,
        ['no_graffiti', 'graffiti'],
        f"{name}_average_confusion_matrix.png",
    )

file_pointer.close()
