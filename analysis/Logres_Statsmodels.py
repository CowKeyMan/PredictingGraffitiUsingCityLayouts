import pandas as pd
import statsmodels.api as sm

fold_amount = 5
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
target_value = 'graffiti_count'

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
#print('df', df)
#df.loc[df['graffiti_count']>1, 'graffiti_count']=1
#df.loc[df['graffiti_count']<1, 'graffiti_count']=0
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)

#print(df.to_string())
xtrain = df[['highest_elevation_m', 'area_m2', 'sub_buildings','nearby_buildings_count','nearby_graffiti_count',
             'nearby_graffiti_average','nearby_graffiti_buildings','nearby_buildings_average_height','nearby_buildings_median_height',
             'nearby_buildings_total_sub_buildings','nearby_buildings_average_sub_buildings','nearby_buildings_median_sub_buildings',
             'nearby_street_lights']]
ytrain = df[['graffiti_count']]

log_reg = sm.Logit(ytrain, xtrain).fit()

print('log_reg', log_reg)
print('log_reg_summary', log_reg.summary())
