import pandas as pd
import sys
sys.path.append('machine_learning')
from utils import scale_features, continuous_variables
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv('buildings_model_features.csv')
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)
df, _ = scale_features(df, None, continuous_variables)


correlations = df.corr()
cmap = sb.cubehelix_palette(light=1, as_cmap=True)

p = sb.heatmap(correlations, fmt='.2f', cmap=cmap, cbar_kws={"shrink": .82},
                  linewidths=0.1, linecolor='gray')
p.set_yticklabels(p.get_ymajorticklabels(), fontsize=5)
p.set_xticklabels(
    p.get_xmajorticklabels(), fontsize=5, rotation=40, ha="right"
)

p.set_xlabel("X-Features", fontsize=1)
p.set_ylabel("Y-Features", fontsize=1)
p.set_title("Correlation Between Features", fontsize=20)
plt.figure(num=None, figsize=(10, 10))
plt.savefig('correlation_between_features.png')
plt.show()
