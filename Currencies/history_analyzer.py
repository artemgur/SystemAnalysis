import pandas as pd
import numpy as np

from expression.collections import Seq

import load_data
from basket import get_baskets, Basket
import constants
from utilities import seq_to_numpy
import criterions


_week_length = 6


def strategy_state(strategy_number, profit, most_risky_number):
    if strategy_number == most_risky_number:
        if profit >= constants.a:
            return 0
        return 1
    if profit >= constants.a:
        return 2
    return 3


def label_weeks(data: pd.DataFrame):
    data['week'] = data.apply(lambda x: int(x.name) // _week_length, axis=1)
    return data


def calculate_profit_dispersion(dfs: list[pd.DataFrame], baskets: list[Basket]):
    data_weeks = Seq(dfs).map(lambda x: x.groupby('week').agg({'<OPEN>': 'first', '<CLOSE>': 'last'})).to_list()
    profits_matrix = np.zeros((4, 4))
    counts_matrix = np.zeros((4, 4))
    for week in data_weeks[0].index:
        profits = seq_to_numpy(
            Seq(baskets).map(lambda x: x.calculate_profit(
                seq_to_numpy(Seq(data_weeks).map(lambda y: y.loc[week, '<OPEN>'])),
                seq_to_numpy(Seq(data_weeks).map(lambda y: y.loc[week, '<CLOSE>']))
            ))
        )

        most_risky = seq_to_numpy(Seq(baskets)
                              .map(lambda x: x.calculate_risk(np.column_stack(Seq(dfs)
                              .map(lambda y: y.query(f'week == {week}')['<CLOSE>'].to_numpy()).to_list()))))\
                              .argmax()
        if profits[most_risky] > 0:
            profits[most_risky] *= 0.3

        strategy_state_points = Seq(profits).mapi(lambda i, x: (i, strategy_state(i, x, most_risky)))

        for point in strategy_state_points:
            profits_matrix[point[0], point[1]] += profits[point[0]]
            counts_matrix[point[0], point[1]] += 1

    # Needed to avoid division by 0 errors. Source: https://stackoverflow.com/questions/26248654/how-to-return-0-with-divide-by-zero
    avg_profits_matrix = np.divide(profits_matrix, counts_matrix, out=np.zeros_like(profits_matrix), where=counts_matrix != 0)
    total_count = counts_matrix.sum(axis=1)
    probabilities_matrix = counts_matrix / total_count[:, None]
    return avg_profits_matrix, probabilities_matrix


def handle_missing_days(dfs: list[pd.DataFrame]):
    dfs = list(Seq(dfs).map(lambda x: x.set_index('<DATE>')))
    for i in range(len(dfs)):
        for j in range(i + 1, len(dfs)):
            dfs[i], dfs[j] = dfs[i].align(dfs[j], axis=0)
    return Seq(dfs).map(lambda x: x.fillna(method='ffill'))


# noinspection SpellCheckingInspection
def calculate_matrixes():
    dfs = list(load_data.load())
    dfs = list(handle_missing_days(dfs).map(label_weeks))
    baskets = list(get_baskets())
    avg_profits_matrix, probabilities_matrix = calculate_profit_dispersion(dfs, baskets)
    return avg_profits_matrix, probabilities_matrix


def calculate_best_strategies(avg_profits_matrix, probabilities_matrix):
    best_strategies = [criterions.maximin(avg_profits_matrix), criterions.maximax(avg_profits_matrix),
                       criterions.hurwicz(avg_profits_matrix, 0.25), criterions.hurwicz(avg_profits_matrix, 0.5),
                       criterions.hurwicz(avg_profits_matrix, 0.75), criterions.savage(avg_profits_matrix),
                       criterions.bayes(avg_profits_matrix, probabilities_matrix)]
    return best_strategies







