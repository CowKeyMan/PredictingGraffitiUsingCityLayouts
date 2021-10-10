"""
Extracting street details from public-scteets csv and
cleaning it up to our standard format
"""

import pandas as pd


def lower_and_underscore(string):
    return string.lower().replace(' ', '_')


def split_streetnames(x):
    s = x.split()
    if len(s) > 1:
        return ' '.join(s[1:])
    return x


# load street data and convert street blocks to whole streets
# if street with multiply types take mode
df = pd.read_csv('resources/data/original/public-streets.csv', sep=';')
df['street'] = df['HBLOCK'].map(split_streetnames)
df['street_type'] = df['STREETUSE']
df = df[['street', 'street_type']]
df['street_type'] = df['street_type'].map(lower_and_underscore)
df = df.groupby(['street'], as_index=False).agg(lambda x: pd.Series.mode(x)[0])

df.to_csv('resources/data/generated/street_details.csv', index=False)
