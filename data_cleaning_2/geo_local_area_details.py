import pandas as pd
from area import area
import json


df_area = pd.read_csv(
    'resources/data/original/local-area-boundary.csv',
    delimiter=';'
)
df_area['area_m2'] = df_area.apply(
    lambda row: round(area(json.loads(row['Geom'])), 2),
    axis=1
)
df_area['geo_local_area'] = df_area['Name']
df_area = df_area[['geo_local_area', 'area_m2']]

df_pop = pd.read_csv('resources/data/original/census2016.csv')
df_pop = df_pop.iloc[0, 2:24]
df_pop = df_pop.apply(lambda x: int(x.replace(',', '')))
df_pop = df_pop.reset_index()
df_pop = df_pop.rename(columns={'index': 'Name', 0: 'population'})
df_pop['geo_local_area'] = df_pop['Name'].apply(lambda x: x.strip())
df_pop = df_pop[['geo_local_area', 'population']]

df = df_area.merge(df_pop, on='geo_local_area')
df['pop_density'] = df['population'] / df['area_m2']
df.to_csv('resources/data/generated/geo_local_area_details.csv', index=False)
