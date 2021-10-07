import pandas as pd


def split_streetnames(x):
  s = x.split()
  if len(s) > 1:
    return ' '.join(s[1:])
  return x


# Load buildings data
bf = pd.read_csv('resources/data/graffiti_combined_buildings_area_m2.csv')
bf = bf[bf['Type'] == 'B']
b_area = bf.groupby('Geo Local Area', as_index=False).sum()
b_area = b_area[['Geo Local Area', 'area_m2']]

#load street data and convert street blocks to whole streets 
#if street with multiply types take mode
sf = pd.read_csv('resources/data/public-streets.csv', sep=';')
sf['HBLOCK'] = sf['HBLOCK'].map(split_streetnames)
sf['street'] = sf['HBLOCK']
sf['street_type'] = sf['STREETUSE']
sf = sf[['street', 'street_type']].drop_duplicates().sort_values('street')
sf = sf.groupby(['street'], as_index=False).agg(lambda x: pd.Series.mode(x)[0])

# population density and area of local areas
# calculate building coverage ratio: building area / area of local area
pf = pd.read_csv('resources/data/local_area_population.csv')
pf['Geo Local Area'] = pf['Name']
pf = pf.merge(b_area, 'left', on='Geo Local Area')
pf['building_ratio'] = pf['area_m2_y'] / pf['area_m2_x']
pf['area_m2'] = pf['area_m2_x']
pf = pf[['Geo Local Area', 'area_m2', 'pop_density', 'building_ratio']]

#merge dataframes
df_combined = bf.merge(sf, 'left', on='street')
df_combined = df_combined.merge(pf, 'left', on='Geo Local Area')

#Write to CSV
df_combined.to_csv('resources/data/combined_streets.csv', index=False)

