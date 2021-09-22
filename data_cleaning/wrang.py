import pandas as pd
import numpy as np
import json

#Convert Geolocation to Tuple (x,y)
def conv_to_Point(val):
  val = json.loads(val)
  (x,y) = (val['coordinates'])
  return (x,y)

#Find nearest coordinate
def findNearest(row, df):
  if isinstance(row[2], float):
    (x0, y0) = row[0]
    nearest = min(df['Geolocation'], key=lambda x:
      (x[0] - x0)**2 + (x[1] - y0)**2)
    lc = df[df['Geolocation'] == nearest]['Local Area'].item()
    return (row[0], row[1], lc, row[3])
  return row

columns=['Geolocation', 'Type', 'Local Area', 'Count']

#Load required csv:s
graf = pd.read_csv("resources/data/graffiti.csv", sep=';')
prop = pd.read_csv("resources/data/property-addresses.csv", sep=';')
stlig = pd.read_csv("resources/data/street-lighting-poles.csv", sep=';')

#Convert Geolocation
graf['Geom'] = graf['Geom'].map(conv_to_Point)
stlig['Geom'] = stlig['Geom'].map(conv_to_Point)
prop['Geom'] = prop['Geom'].map(conv_to_Point)

#Convert to same form [Geolocation | Type | Local Area | Count]
graf = pd.DataFrame({'Geolocation': graf['Geom'], 'Type': 'G', 'Local Area': graf['Geo Local Area'], 'Count': graf['COUNT']})
stlig = pd.DataFrame({'Geolocation': stlig['Geom'], 'Type': 'L', 'Local Area': stlig['Geo Local Area'], 'Count': stlig['NODE_NUMBER']})
prop = pd.DataFrame({'Geolocation': prop['Geom'], 'Type': 'P', 'Local Area': prop['Geo Local Area'], 'Count': 1})

#Fix missing values in Local Area
#Graffiti
nonNa = graf.dropna()
mgraf = pd.DataFrame([
  findNearest(row, nonNa) for row in zip(graf['Geolocation'], graf['Type'], graf['Local Area'], graf['Count'])
], columns=columns)

#Street Lightning
nonNa = stlig.dropna()
stlig = pd.DataFrame([
  findNearest(row, nonNa) for row in zip(stlig['Geolocation'], stlig['Type'], stlig['Local Area'], stlig['Count'])
], columns=columns)

#Property
nonNa = prop.dropna()
prop = pd.DataFrame([
  findNearest(row, nonNa) for row in zip(prop['Geolocation'], prop['Type'], prop['Local Area'], prop['Count'])
], columns=columns)


#Combine fixed datasets & write to csv
res = pd.concat([graf, stlig, prop])
#graf.to_csv('F_graffiti.csv')
#stlig.to_csv('F_propertyA.csv')
#stlig.to_csv('F_streetL.csv')
res['Latitude'] = [x[0] for x in res['Geolocation']]
res['Longitude'] = [x[1] for x in res['Geolocation']]
res.drop(columns=['Geolocation'], inplace=True)
res.to_csv('resources/data/graffiti_combined.csv', index=False)
