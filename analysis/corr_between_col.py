import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
#df = pd.read_csv('buildings_model_features.csv')
#print('df', df)
#df.loc[df['graffiti_count']>1, 'graffiti_count']=1
#df.loc[df['graffiti_count']<1, 'graffiti_count']=0

correlations = df.corr()
print('correlations', correlations.to_string())
sb.heatmap(correlations)
plt.show()
correlations.to_csv('resources/data/generated/correlation_between_columns.csv', index=False)

#correlations.to_csv('correlation_between_columns.csv', index=False)
