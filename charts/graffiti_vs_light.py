"""
Draw a scatter plot and line of best fit of the number
of graffiti against the number of light sources.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read CSV
df = pd.read_csv(
    'resources/data/graffiti_combined.csv',
    dtype={
        'Geo Local Area': str,
        'Count': int,
        'SITE_ID': str,
        'Latitude': float,
        'Longitude': float,
        'Type': str,
    }
)

# Drop unecessary columns
df = df[['Type', 'Geo Local Area', 'Count']]

# Change both street lighting and buildings type to 'L'
df['Type'].replace({'S': 'L', 'B': 'L'}, inplace=True)

grouped_values = []
# Group based on 'Geo Local Area' and count light sources and graffiti amount
for area in df['Geo Local Area'].unique():
    df_area = df[df['Geo Local Area'] == area]
    light_amount = df_area[df_area['Type'] == 'L']['Count'].sum()
    graffiti_amount = df_area[df_area['Type'] == 'G']['Count'].sum()
    grouped_values.append([area, light_amount, graffiti_amount])
df = pd.DataFrame(
    grouped_values,
    columns=['Geo Local Area', 'Light Sources', 'Graffiti Count']
)

# plot
fig, scatter = plt.subplots(figsize=(10, 6), dpi=100)
scatter \
    = sns.regplot(x='Light Sources', y='Graffiti Count', data=df, fit_reg=True)
plt.show()
fig.savefig('resources/images/graffiti_vs_light_sources.png')
