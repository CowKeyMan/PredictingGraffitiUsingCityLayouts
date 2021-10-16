import pandas as pd
import statsmodels.api as sm
from utils import regularize_features

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
y = df['graffiti_count']
x = df.drop(columns=['graffiti_count'])
x = x.drop(columns=df.iloc[:, 20:42])

print('x', x)
print('y', y)
log_reg = sm.Logit(y, x).fit()

print('log_reg', log_reg)
print('log_reg_summary', log_reg.summary())
