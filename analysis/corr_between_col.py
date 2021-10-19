import pandas as pd
import statsmodels.api as sm
from utils import regularize_features
import seaborn as sb
import matplotlib.pyplot as plt

continuous_variables = [
    'highest_elevation_m',
    'area_m2',
    'sub_buildings',
    'nearby_buildings_count',
    'nearby_graffiti_count',
    'nearby_graffiti_average',
    'nearby_graffiti_buildings',
    'nearby_buildings_average_height',
    'nearby_buildings_median_height',
    'nearby_buildings_total_sub_buildings',
    'nearby_buildings_average_sub_buildings',
    'nearby_buildings_median_sub_buildings',
    'nearby_street_lights',
    'geo_local_area_area_m2',
    'geo_local_area_population',
    'pop_density',
]

df = pd.read_csv('buildings_model_features.csv')
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)
df, _ = regularize_features(df, None, continuous_variables)



correlations = df.corr()
cmap = sb.cubehelix_palette(light=1, as_cmap=True)

p = sb.heatmap(correlations,fmt='.2f', cmap=cmap, cbar_kws={"shrink": .82},
                  linewidths=0.1, linecolor='gray')
p.set_yticklabels(p.get_ymajorticklabels(), fontsize = 5)
p.set_xticklabels(p.get_xmajorticklabels(), fontsize = 5, rotation=40, ha="right")

p.set_xlabel("X-Features", fontsize = 1)
p.set_ylabel("Y-Features", fontsize = 1)
p.set_title("Correlation Between Features", fontsize = 20)
plt.figure(num=None, figsize=(10, 10))
plt.savefig('correlation_between_features.png')
plt.show()