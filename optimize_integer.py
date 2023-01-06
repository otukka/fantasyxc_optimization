import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cvxpy as cp

from filters import *


def get_problem(n, mu, sigma, price, gender):
    w = cp.Variable(n, boolean=True)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T@w
    risk = cp.quad_form(w, sigma)
    prob = cp.Problem(cp.Maximize(ret - gamma*risk),
                      [cp.sum(w) <= 16.0, w >= 0, w <= 1, cp.sum(w.T@price) <= 1, cp.sum(w.T@gender[:, 0]) <= 8.0, cp.sum(w.T@gender[:, 1]) <= 8.0])

    return (w, gamma, prob, ret, risk)


def optimize(mu, sigma, epsilon, price, gender):
    n = len(mu)
    w, gamma, prob, ret, _ = get_problem(n, mu, sigma, price, gender)
    gamma.value = epsilon
    prob.solve(solver='ECOS_BB')
    return (w.value, ret.value)


def run(df, type):

    if type == 'Sprint':
        df = get_sprints(df)
    elif type == 'Distance':
        df = get_distances(df)

    scale = 10**5

    gender = np.zeros((df.shape[0], 2))

    gender[df['athlete.gender'] == 'f', 0] = 1
    gender[df['athlete.gender'] == 'm', 1] = 1

    values = df.select_dtypes(include=np.number).values[:, 2:-1]

    values = values.T / 100

    price = df.select_dtypes(include=np.number).values[:, 1].T

    price = price / scale
    names = df.loc[:, 'athlete.name'].values

    mu = values.mean(axis=0)

    sigma = np.cov(values, rowvar=False)

    risk = 0
    (w, ret) = optimize(mu, sigma, risk, price, gender)

    weight = pd.DataFrame({'Skier': names, 'Weight': w, "Price": price*scale})

    print(weight[weight['Weight'] > 0.2])
    print(weight[weight['Weight'] > 0.2]['Price'].sum())


def main():

    df = get_df('output/filtered_dataset.csv')

    # type = 'Sprint'
    type = 'Distance'

    run(df, type)


if __name__ == "__main__":
    main()
