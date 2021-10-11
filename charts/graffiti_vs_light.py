"""
Draw a scatter plot and line of best fit of the number
of graffiti against the number of light sources.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def lower_and_underscore(string):
    return string.lower().replace(' ', '_')


# street lights
df_lights = pd.read_csv(
    'resources/data/original/street-lighting-poles.csv', delimiter=';'
)
df_lights = df_lights[['Geo Local Area']].dropna()
df_lights['geo_local_area'] \
    = df_lights['Geo Local Area'].map(lower_and_underscore)
df_lights_to_merge = df_lights.groupby('geo_local_area').size() \
    .reset_index(name='street_light_counts')

# buildings
df_buildings \
    = pd.read_csv('resources/data/generated/buildings_all_features.csv')
df_buildings['geo_local_area'] \
    = df_buildings['geo_local_area'].map(lower_and_underscore)
df_buildings_to_merge = df_buildings.groupby('geo_local_area').size() \
    .reset_index(name='building_counts')

# graffiti
df_graffiti_to_merge = df_buildings[['graffiti_count', 'geo_local_area']] \
    .groupby('geo_local_area').sum().reset_index()

# merge

df = df_lights_to_merge\
    .merge(df_buildings_to_merge, on='geo_local_area') \
    .merge(df_graffiti_to_merge, on='geo_local_area')
df['Lights'] = df['street_light_counts'] + df['building_counts']
df['Graffiti'] = df['graffiti_count']

# plot
fig, scatter = plt.subplots(figsize=(10, 6), dpi=100)
scatter \
    = sns.regplot(x='Lights', y='Graffiti', data=df, fit_reg=True)
plt.show()
fig.savefig('resources/images/graffiti_vs_light_sources.png')
