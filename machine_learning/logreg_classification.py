import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)
y = df['graffiti_count']
x = df.drop(columns=['graffiti_count'])

log_reg = sm.Logit(y, x).fit()

print('log_reg', log_reg)
print('log_reg_summary', log_reg.summary())
