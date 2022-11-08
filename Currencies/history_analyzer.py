import pandas as pd
import numpy as np

from expression.collections import Seq

import load_data
from basket import get_baskets, Basket
import constants


_week_length = 6


def strategy_state(strategy_number, profit, most_risky_number):
    if strategy_number == most_risky_number:
        if profit >= constants.a: # TODO check where equality should be
            return 0
        return 1
    if profit >= constants.a: # TODO check where equality should be
        return 2
    return 3



def label_weeks(data: pd.DataFrame):
    data['week'] = data.apply(lambda x: int(x.name) // _week_length, axis=1)
    return data

def temp_f(week, x):
    #try:
    a = np.column_stack(x)
    #except:
    #    print(week, x)
    return a


def calculate_profit_dispersion(dfs: list[pd.DataFrame], baskets: list[Basket]):
    data_weeks = Seq(dfs).map(lambda x: x.groupby('week').agg({'<OPEN>': 'first', '<CLOSE>': 'last'})).to_list()
    profits_matrix = np.zeros((4, 4))
    counts_matrix = np.zeros((4, 4))
    for week in data_weeks[0].index:
        profits = np.array(
            Seq(baskets).map(lambda x: x.calculate_profit(
                np.array(Seq(data_weeks).map(lambda y: y.loc[week, '<OPEN>']).to_list()),
                np.array(Seq(data_weeks).map(lambda y: y.loc[week, '<CLOSE>']).to_list())
            )).to_list()
        )
        #profits_sum += profits

        most_risky = np.array(Seq(baskets)
                              .map(lambda x: x.calculate_risk(temp_f(week, Seq(dfs)
                              .map(lambda y: y.query(f'week == {week}')['<CLOSE>'].to_numpy()).to_list()))).to_list())\
                              .argmax()
        print(most_risky)

        strategy_state_points = Seq(profits).mapi(lambda i, x: (i, strategy_state(i, x, most_risky)))

        #result_profits_matrix = np.zeros((4, 4))
        #result_counts_matrix = np.zeros((4, 4))

        for point in strategy_state_points:
            profits_matrix[point[0], point[1]] += profits[point[0]]
            counts_matrix[point[0], point[1]] += 1

    # Needed to avoid division by 0 errors. Source: https://stackoverflow.com/questions/26248654/how-to-return-0-with-divide-by-zero
    avg_profits_matrix = np.divide(profits_matrix, counts_matrix, out=np.zeros_like(profits_matrix), where=counts_matrix != 0)
    total_count = counts_matrix.sum(axis=1) # TODO check axis
    probabilities_matrix = counts_matrix / total_count[:, None] # TODO check shape broadcast
    return avg_profits_matrix, probabilities_matrix


def handle_missing_days(dfs: list[pd.DataFrame]):
    dfs = list(Seq(dfs).map(lambda x: x.set_index('<DATE>')))
    for x in range(len(dfs)):
        for y in range(x + 1, len(dfs)):
            dfs[x], dfs[y] = dfs[x].align(dfs[y], axis=0)
    return Seq(dfs).map(lambda x: x.fillna(method='ffill'))


def run():
    dfs = list(load_data.load())
    dfs = list(handle_missing_days(dfs).map(label_weeks))
    for df in dfs:
        print(df.shape)
    #     print('––––––––––––––––––––––––––––––––––––––––')
    # for x in dfs[0]['<OPEN>'].index:
    #     print(x)
    baskets = list(get_baskets())
    avg_profits_matrix, probabilities_matrix = calculate_profit_dispersion(dfs, baskets)
    print(avg_profits_matrix)
    print('–––––––––––––––––––––––––––––––––––––––––––––––––––––')
    print(probabilities_matrix)





