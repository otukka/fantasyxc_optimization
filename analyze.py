import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from filters import *


def points_per_price_gender_athlete(df):

    tmp = df[df['athlete.gender'] == 'f']

    fig, axs = plt.subplots(2)

    fig.suptitle('Points vs Price')

    sns.scatterplot(ax=axs[0], x='points', y='price', data=tmp, label='women')
    axs[0].set(ylabel='price', xlabel='points')
    axs[0].grid(axis='y')
    # axs[0].set(xscale="log", yscale="log")
    axs[0].legend()

    tmp = df[df['athlete.gender'] == 'm']

    sns.scatterplot(ax=axs[1], x='points', y='price', data=tmp, label='men')
    axs[1].set(ylabel='price', xlabel='points')
    axs[1].grid(axis='y')
    # axs[1].set(xscale="log", yscale="log")
    axs[1].legend()

    plt.show()


def points_per_athlete_gender_athlete(df):

    tmp = df[df['athlete.gender'] == 'f'].reset_index()

    fig, axs = plt.subplots(2)

    fig.suptitle('Points vs Athlete')

    sns.lineplot(ax=axs[0], y='points', x=tmp.index, data=tmp, label='women')
    axs[0].set(xlabel='athlete ordered by points', ylabel='points')
    axs[0].grid(axis='y')
    axs[0].legend()

    tmp = df[df['athlete.gender'] == 'm']

    sns.lineplot(ax=axs[1], y='points', x=tmp.index, data=tmp, label='men')
    axs[1].set(xlabel='athlete ordered by points', ylabel='points')
    axs[1].grid(axis='y')
    axs[1].legend()

    plt.show()


def price_per_athlete_gender_athlete(df):

    tmp = df[df['athlete.gender'] == 'f'].reset_index()

    fig, axs = plt.subplots(2)

    fig.suptitle('Price vs Athlete')

    sns.lineplot(ax=axs[0], y='price', x=tmp.index, data=tmp, label='women')
    axs[0].set(xlabel='athlete ordered by points', ylabel='price')
    axs[0].grid(axis='y')
    axs[0].legend()

    tmp = df[df['athlete.gender'] == 'm']

    sns.lineplot(ax=axs[1], y='price', x=tmp.index, data=tmp, label='men')
    axs[1].set(xlabel='athlete ordered by points', ylabel='price')
    axs[1].grid(axis='y')
    axs[1].legend()

    plt.show()


def main():

    df = get_df().sort_values('points').reset_index()

    points_per_price_gender_athlete(df)
    points_per_athlete_gender_athlete(df)
    price_per_athlete_gender_athlete(df)


if __name__ == "__main__":
    main()
