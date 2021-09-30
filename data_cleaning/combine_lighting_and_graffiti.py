import pandas as pd
import json
from geopy.distance import geodesic
import multiprocessing
from pathlib import Path


def conv_to_point(val):
    lon, lat = json.loads(val)['coordinates']
    return lat, lon


# find nearest coordinate
def find_nearest(row: pd.Series, df_non_na: pd.DataFrame) -> str:
    if not pd.isnull(row['Geo Local Area']):
        return row['Geo Local Area']
    return min(
        df_non_na['Geom'],
        key=lambda lat_lon: geodesic(lat_lon, row['Geom'])
    )


def chunk_find_nearest(
    index: int,
    df: pd.DataFrame,
    df_non_na: pd.DataFrame,
) -> None:
    # df['Geo Local Area'] = [
    #     find_nearest(row[1], df_non_na) for row in df.iterrows()
    # ]
    result = []
    for i, row in enumerate(df.iterrows()):
        if i % 10 == 0:
            print(f'{index}: {i + 1}/{len(df)}')
        result.append(find_nearest(row[1], df_non_na))
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
    jobs = 8
    processes = []
    df_non_na = df[['Geom', 'Geo Local Area']].dropna()
    # shuffle to get (almost) equal workload
    df = df.sample(frac=1, ignore_index=True)
    # split dataframes into chunks and process them individually
    chunk_size = len(df) / jobs
    for j in range(jobs):
        chunk = df.iloc[round(j * chunk_size): round((j + 1) * chunk_size)]
        process = multiprocessing.Process(
            target=chunk_find_nearest,
            args=[j, chunk, df_non_na],
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
