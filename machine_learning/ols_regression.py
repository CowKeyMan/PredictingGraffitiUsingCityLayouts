import pandas as pd
import statsmodels.formula.api as smf
from utils import regularize_features
import itertools


def build_formula(x):
    s = ''
    for t, z in itertools.combinations(x, 2):
        s += " + " + t + ':' + z
    return s


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

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
df, _ = regularize_features(df, None, continuous_variables)
y = df['graffiti_count']
x = df.drop(columns=['graffiti_count'])

singular_variables = ' + '.join(x.columns.tolist())
joint_variables = build_formula(x.columns.tolist())
# formula = "graffiti_count ~ " + s + joint_variables
formula = "graffiti_count ~ " + singular_variables

fit = smf.ols(formula, data=df).fit()
print(fit.summary())
