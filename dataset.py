

import pandas as pd
import numpy as np

from pathlib import Path

from filters import get_df

def races():
    p = Path('output/races')
    files = p.glob('*.csv')

    dfs = []
    for file in files:
        dfs.append(pd.read_csv(file))

    df = pd.concat(dfs, axis=0, ignore_index=True)

    df = df[['include_in_total', 'weekend_id', 'discipline',
             'distance', 'scored', 'date', 'selection_id', 'name', 'country',
             'gender', 'race_id']]

    df = df.sort_values(['race_id']).reset_index()

    df = df[df['name'] != "Relay"]

    df.to_csv('output/races.csv')


def results():
    p = Path('output/results')
    files = p.glob('*.csv')

    dfs = []
    for file in files:
        dfs.append(pd.read_csv(file))

    df = pd.concat(dfs, axis=0, ignore_index=True)

    df = df[['athlete_id', 'race_id', 'score', 'rank',
            'athlete.price', 'athlete.active', 'athlete.is_team',
             'athlete.name', 'athlete.athlete_id', 'athlete.country',
             'athlete.gender', 'athlete.score', 'athlete.rank']]

    df = df[df['athlete.is_team'] == False]

    df = df.sort_values(['race_id']).reset_index()

    df.to_csv('output/results.csv')


def merge():

    races = pd.read_csv('output/races.csv')
    results = pd.read_csv('output/results.csv')
    prices = pd.read_csv('output/prices.csv')

    results = results.merge(
        prices, how='left', on='athlete_id', validate='m:1')

    df = results.merge(races, how='outer', on='race_id')

    df = pd.pivot(df, index=['athlete_id', 'athlete.name', 'athlete.gender', 'price'], columns=[
                  'race_id', 'discipline', 'name'], values=['score'])

    df['points'] = df.select_dtypes(include=np.number).sum(axis=1)

    df = df.sort_values(['athlete.gender', 'points'], ascending=[
                        True, False]).reset_index()

    df = df.fillna(0)

    df.to_csv('output/dataset.csv')

def athletes(filename):
    attendes = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            attendes.append(line.replace('\n', '').rstrip())
    
    return attendes

def filter_athletes():

    df = get_df()

    names = athletes('input/07.01.2023.txt')

    df = df[df['athlete.name'].isin(names)]

    df = df.reset_index(drop=True)

    df.to_csv('output/filtered_dataset.csv')


def main():
    races()
    results()
    merge()
    filter_athletes()

if __name__ == "__main__":
    main()
