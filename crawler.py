

import requests
import requests_cache
from pathlib import Path
import pandas as pd
import datetime

START_ID = 741
END_ID = 772

def main():

    session = requests_cache.CachedSession('fantasyxc')

    # Race results

    path = Path('output/results')
    if not path.exists():
        Path.mkdir(path, parents=True)

    for i in range(START_ID, END_ID):
        r = session.get('https://www.fantasyxc.se/api/races/'+str(i)+'/results/athletes')

        df = pd.json_normalize(r.json())

        df.to_csv(path.joinpath(str(i)+'.csv'))

    # Races

    path = Path('output/races')
    if not path.exists():
        Path.mkdir(path, parents=True)

    for i in range(START_ID, END_ID):
        r = session.get('https://www.fantasyxc.se/api/races/'+str(i))

        df = pd.json_normalize(r.json())

        df.to_csv(path.joinpath(str(i)+'.csv'))

    # Athlete prices

    path = Path('output/prices')
    if not path.exists():
        Path.mkdir(path, parents=True)

    r = requests.get(r"https://www.fantasyxc.se/api/athletes?filter_active=True&country=!RUS&country=!BLR")

    df = pd.json_normalize(r.json())

    df = df[['athlete_id', 'price']]
    date = '{0:%Y-%m-%d}'.format(datetime.datetime.now().date())
    df.to_csv('output/prices/' + date + '.csv')
    df.to_csv('output/prices.csv')


if __name__ == "__main__":
    main()