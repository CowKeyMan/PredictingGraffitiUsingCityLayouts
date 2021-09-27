import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

#Read Lighting Poles and Graffiti
lighting_csv = pd.read_csv('resources/data/street-lighting-poles.csv', delimiter=';')
graffiti_csv = pd.read_csv('resources/data/graffiti.csv', delimiter=';')

#Drop unneeded columns
lighting_csv = lighting_csv.drop(['BLOCK_NUMBER', 'Geom'], axis = 1)
graffiti_csv = graffiti_csv.drop(['Geom'], axis = 1)

#Group by based on 'Geo Local Area'
lighting_csv = lighting_csv.groupby(['Geo Local Area'])['NODE_NUMBER'].count()
graffiti_csv = graffiti_csv.groupby('Geo Local Area')['COUNT'].sum()

#Merging two datasets (Graffiti and Lighting)
df = pd.merge(graffiti_csv, lighting_csv, on='Geo Local Area')

#Trying using seaborn
#fig, scatter = plt.subplots(figsize = (10,6), dpi = 100)
#scatter = sb.scatterplot(x='COUNT', y= 'NODE_NUMBER', data = df, hue='Geo Local Area', legend = True)
'''scatter.legend(fontsize = 6, \
               bbox_to_anchor= (1.03, 1), \
             #  title="Graffity", \
             #  title_fontsize = 18, \
               shadow = True, \
               facecolor = 'white')
'''

#Trying using Pyplot, using gaussian_kde to estimate the probability density function (PDF) of a random variable in a non-parametric way
xy = np.vstack([df['COUNT'], df['NODE_NUMBER']])
z = gaussian_kde(xy)(xy)
fig, ax = plt.subplots()
ax.scatter(df['COUNT'], df['NODE_NUMBER'], c=z, s=100)
plt.show()
