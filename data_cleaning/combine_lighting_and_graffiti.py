"""
Read graffiti, street-lighting-poles and property-addresses csvs
and combine them. Fill in missing Geo Local Area to be the closest location
available based on other object's Area. Save them to 'graffiti-combined.csv'
"""

import pandas as pd
import json
# from geopy.distance import geodesic
import multiprocessing
from pathlib import Path
import argparse


argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-j", "--jobs", required=False, default=6, type=int
)
jobs = vars(argparser.parse_known_args()[0])['jobs']


def conv_to_point(val):
    lon, lat = json.loads(val)['coordinates']
    return lat, lon


# find nearest coordinate
def find_nearest(row: pd.Series, dict_non_na: dict) -> str:
    if not pd.isnull(row['Geo Local Area']):
        return row['Geo Local Area']
    return min(
        dict_non_na,
        # key=lambda r: geodesic(r['Geom'], row['Geom'])
        key=lambda r: (
            (r['Latitude'] - row['Latitude']) ** 2
            + (r['Longitude'] - row['Longitude']) ** 2
        )
    )['Geo Local Area']


def chunk_find_nearest(
    index: int,
    df: pd.DataFrame,
    dict_non_na: dict,
) -> None:
    # This does the same as the lines below, but without logging
    # df['Geo Local Area'] = [
    #     find_nearest(row[1], df_non_na) for row in df.iterrows()
    # ]
    result = []
    dictionary = df.to_dict('records')
    for i, row in enumerate(dictionary):
        if i % 1000 == 0:
            print(f'{index}: {i + 1}/{len(df)}', flush=True)
        result.append(find_nearest(row, dict_non_na))
    df['Geo Local Area'] = result
    df.to_csv(f'resources/data/temp_{index}.csv', index=False)


if __name__ == '__main__':
    # load required csvs
    graf = pd.read_csv("resources/data/graffiti.csv", sep=';')
    prop = pd.read_csv("resources/data/property-addresses.csv", sep=';')
    stlig = pd.read_csv("resources/data/street-lighting-poles.csv", sep=';')

    # convert Geolocation
    graf['Geom'] = graf['Geom'].map(conv_to_point)
    stlig['Geom'] = stlig['Geom'].map(conv_to_point)
    prop['Geom'] = prop['Geom'].map(conv_to_point)

    # add type
    graf['Type'] = 'G'
    stlig['Type'] = 'L'
    prop['Type'] = 'B'

    # add Count column for each of the objects
    stlig['Count'] = 1
    prop['Count'] = 1
    graf['Count'] = graf['COUNT']

    # concatenate
    df = pd.concat([graf, stlig, prop], ignore_index=True)

    # get latitude and longitude
    df['Latitude'] = [x[0] for x in df['Geom']]
    df['Longitude'] = [x[1] for x in df['Geom']]

    # drop unecessary columns
    df = df[
        'Geo Local Area,Count,SITE_ID,Latitude,Longitude,Geom,Type'.split(',')
    ]

    # fix missing values in Local Area - single threaded
    # df['Geo Local Area'] = [
    #     find_nearest(row[1], df[['Geom', 'Geo Local Area']].dropna())
    #     for row in df.iterrows()
    # ]

    # fix missing values in Local Area - multi threaded
    # setup multiprocessing parameters
    processes = []
    df_non_na \
        = df[['Geom', 'Geo Local Area', 'Longitude', 'Latitude']].dropna()
    # shuffle to get (almost) equal workload
    df = df.sample(frac=1, ignore_index=True)
    # split dataframes into chunks and process them individually
    chunk_size = len(df) / jobs
    for j in range(jobs):
        chunk = df.iloc[round(j * chunk_size): round((j + 1) * chunk_size)]
        process = multiprocessing.Process(
            target=chunk_find_nearest,
            args=[j, chunk, df_non_na.to_dict('records')],
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    # read the processed dataframes from disk
    df = pd.concat(
        [
            pd.read_csv(f'resources/data/temp_{index}.csv')
            for index in range(jobs)
        ],
        ignore_index=True
    )
    for index in range(jobs):
        Path(f'resources/data/temp_{index}.csv').unlink()

    # write result to csv
    df.drop(columns=['Geom'], inplace=True)
    df.sort_values('Type', inplace=True)
    df.to_csv('resources/data/graffiti_combined.csv', index=False)
