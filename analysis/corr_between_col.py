# Testing

import pandas as pd
import statsmodels.api as sm
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv('buildings_model_features.csv')
print('df', df)

#print(df.to_string())

xtrain = df[['highest_elevation_m', 'area_m2', 'sub_buildings','nearby_buildings_count','nearby_graffiti_count',
             'nearby_graffiti_average','nearby_graffiti_buildings','nearby_buildings_average_height','nearby_buildings_median_height',
             'nearby_buildings_total_sub_buildings','nearby_buildings_average_sub_buildings','nearby_buildings_median_sub_buildings',
             'nearby_street_lights','graffiti_count']]
ytrain = df[['geo_local_area_Arbutus-Ridge']]

log_reg = sm.Logit(ytrain, xtrain).fit()

print('log_reg', log_reg)
print('log_reg_summary', log_reg.summary())

correlations = df.corr()
print('correlations', correlations.to_string())
sb.heatmap(correlations)
plt.show()