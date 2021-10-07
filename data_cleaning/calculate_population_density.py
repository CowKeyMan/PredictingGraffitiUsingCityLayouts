import pandas as pd

df = pd.read_csv('resources/data/geolocal_area_m2.csv')

area_pop = pd.read_csv('resources/data/census2016.csv')
area_pop = area_pop.iloc[0,2:24]
area_pop = area_pop.apply(lambda x: int(x.replace(',','')))
area_pop = area_pop.reset_index()
area_pop = area_pop.rename(columns={'index': 'Name', 0: 'population'})
area_pop['Name'] = area_pop['Name'].apply(lambda x: x.strip())

df = df.merge(area_pop, on='Name')
df['pop_density'] =  df['population'] / df['area_m2'] * 1000000
df.to_csv('resources/data/local_area_population.csv',index=False)
