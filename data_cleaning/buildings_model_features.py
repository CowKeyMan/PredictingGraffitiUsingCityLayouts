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
        'lon',
        'geo_local_area',
    ],
    inplace=True
)

to_one_hot_encode = ['roof_type', 'street_type']

for var_name in to_one_hot_encode:
    df = pd.concat([df, pd.get_dummies(df[var_name], prefix=var_name)], axis=1)

df.drop(columns=to_one_hot_encode, inplace=True)

#Replacing graffiti count with 0 and 1
#df.loc[df['graffiti_count']>1, 'graffiti_count']=1
#df.loc[df['graffiti_count']<1, 'graffiti_count']=0

df.to_csv('resources/data/generated/buildings_model_features.csv', index=False)
