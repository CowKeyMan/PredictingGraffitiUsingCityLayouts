"""
Make the csv ready for building models with it by removing unecessary
features such as building_id and one-hot encoding categorical features
"""

import pandas as pd

df = pd.read_csv('resources/data/generated/buildings_all_features.csv')

df.drop(
    columns=[
        'building_id',
        'property_coordinate',
        'street',
        'building_polygon',
        'lat',
        'lon'
    ],
    inplace=True
)

to_one_hot_encode = ['roof_type', 'geo_local_area', 'street_type']

for var_name in to_one_hot_encode:
    df = pd.concat([df, pd.get_dummies(df[var_name], prefix=var_name)], axis=1)

df.drop(columns=to_one_hot_encode, inplace=True)

df.to_csv('resources/data/generated/buildings_model_features.csv', index=False)
