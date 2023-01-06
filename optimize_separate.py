import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cvxpy as cp

from filters import *


def get_problem(n, mu, sigma, price):
    w = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T@w
    risk = cp.quad_form(w, sigma)
    prob = cp.Problem(cp.Maximize(ret - gamma*risk),
                      [cp.sum(w) <= 8.0, w >= 0, w <= 1, cp.sum(w.T@price) <= 1])

    return (w, gamma, prob, ret, risk)


def optimize(mu, sigma, epsilon, price):
    n = len(mu)
    w, gamma, prob, ret, _ = get_problem(n, mu, sigma, price)
    gamma.value = epsilon
    prob.solve(solver='ECOS')
    return (w.value, ret.value)


def men(df, percent, print_=False, type=None, style=None):

    df = get_men(df)

    if style == 'Freestyle':
        df = get_freestyles(df)
    elif style == 'Classic':
        df = get_classics(df)

    if type == 'Sprint':
        df = get_sprints(df)
    elif type == 'Distance':
        df = get_distances(df)

    scale = 10**5 * percent

    return run(df, scale, print_)


def women(df, percent, print_=False, type=None, style=None):

    df = get_women(df)

    if style == 'Freestyle':
        df = get_freestyles(df)
    elif style == 'Classic':
        df = get_classics(df)

    if type == 'Sprint':
        df = get_sprints(df)
    elif type == 'Distance':
        df = get_distances(df)

    scale = 10**5 * percent

    return run(df, scale, print_)


def run(df, scale, print_):

    values = df.select_dtypes(include=np.number).values[:, 2:-1]

    values = values.T / 100

    price = df.select_dtypes(include=np.number).values[:, 1].T

    price = price / scale
    names = df.loc[:, 'athlete.name'].values

    mu = values.mean(axis=0)

    sigma = np.cov(values, rowvar=False)

    risk = 0
    (w, ret) = optimize(mu, sigma, 0, price)

    weight = pd.DataFrame({'Skier': names, 'Weight': w, "Price": price*scale})

    if print_:
        print(weight[weight['Weight'] > 0.2])
        print(weight[weight['Weight'] > 0.2]['Price'].sum())

    price = weight[weight['Weight'] > 0.99999]['Price'].sum()
    count = len(weight[weight['Weight'] > 0.99999])

    return (price, ret, count)


def main():

    df = get_df('output/filtered_dataset.csv')

    # type = 'Sprint'
    type = 'Distance'

    percent = []
    total_price = []
    total_return = []
    count = []

    for i in np.linspace(30, 70, 100):

        percentToWomen = i / 100
        m_p, m_r, m_c = men(df, 1 - percentToWomen, type=type)
        w_p, w_r, w_c = women(df, percentToWomen, type=type)

        percent.append(percentToWomen)
        total_price.append(m_p + w_p)
        total_return.append(m_r + w_r)
        count.append((m_c % 8) + (w_c % 8))

    fig, axs = plt.subplots()
    axs.plot(percent, total_return)
    axs.set(ylabel='return', xlabel='percent')
    axs.grid(axis='y')
    axs.legend()
    plt.show()

    ret_df = pd.DataFrame(
        {'Percent': percent, 'Price': total_price, 'Return': total_return, 'Count': count})

    ret_df['Return %'] = ret_df['Return'] / ret_df['Return'].max()
    print(ret_df)

    print(ret_df[ret_df['Count'] == 0])

    max_percent = ret_df[ret_df['Return %'] == 1]['Percent'].iloc[0]

    print(max_percent)
    _, _, _ = men(df, 1 - max_percent, True, type=type)
    _, _, _ = women(df, max_percent, True, type=type)


if __name__ == "__main__":
    main()
