import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_df(filename='output/dataset.csv'):
    df = pd.read_csv(filename, index_col=[0], header=[0, 1, 2, 3])

    df.columns = pd.MultiIndex.from_frame(df.columns.to_frame().apply(
        lambda x: np.where(x.str.contains('Unnamed'), '', x)).ffill())

    df.index = pd.MultiIndex.from_frame(df.index.to_frame().ffill())

    df = df.infer_objects()

    return df

def get_classics(df):
    return df.drop('Freestyle', axis=1, level=2)
def get_freestyles(df):
    return df.drop('Classic', axis=1, level=2)
def get_sprints(df):
    return df.drop(['Pursuit', 'Individual Start', 'Mass Start'], axis=1, level=3)
def get_distances(df):
    return df.drop('Sprint', axis=1, level=3)
def get_men(df):
    tmp = df[df['athlete.gender'] == 'm']
    # Remove women's races 
    return tmp.loc[:, (tmp != 0).any(axis=0)]
def get_women(df):
    tmp = df[df['athlete.gender'] == 'f']
    # Remove men's races 
    return tmp.loc[:, (tmp != 0).any(axis=0)]

def filter_athletes(df, list):
    return df[~df['athlete.name'].isin(list)]

