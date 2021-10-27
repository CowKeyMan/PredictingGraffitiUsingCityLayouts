import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn.palettes import color_palette

def split_streetnames(x):
    s = x.split()
    if len(s) > 1:
        return ' '.join(s[1:])
    return x


df = pd.read_csv('resources/data/buildings_all_features.csv')
sf = pd.read_csv('resources/data/original/public-streets.csv', sep=';')

df = df[['street_type', 'street', 'graffiti_count', 'geo_local_area']]
df['building'] = 1

gcount = df.groupby('street').sum()
ndf = df.groupby(['street'], as_index=False).agg(lambda x: pd.Series.mode(x)[0]).drop(columns=['graffiti_count','building'])
ndf = ndf.merge(gcount, on='street')
sf['street'] = sf['HBLOCK'].map(split_streetnames)

top_streets = ndf[['street', 'graffiti_count']]
top_streets = top_streets.sort_values('graffiti_count', ascending=False)[:10]
s_ratio = top_streets['graffiti_count'].sum() / ndf['graffiti_count'].sum()
top_streets = top_streets.append(pd.Series({'street': 'REST', 'graffiti_count': ndf['graffiti_count'].sum() - top_streets['graffiti_count'].sum()}), ignore_index=True)
top_s_labels = top_streets['street']

pie_colors = sns.color_palette('Paired')

top_streets.plot.pie(
  labels = top_streets['street'],
  y='graffiti_count',
  colors = pie_colors,
  autopct='%1.1f%%',
  pctdistance = 0.8,
  legend=False,
  ylabel = '',
  fontsize = 18,
)

plt.show()
