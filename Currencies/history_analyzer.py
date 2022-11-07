import pandas as pd
import numpy as np

from expression.collections import Seq

import load_data
from basket import get_baskets, Basket


_week_length = 6


def label_weeks(data: pd.DataFrame):
    data['week'] = data.apply(lambda x: int(x.name) // _week_length, axis=1)
    return data


def calculate_profit_dispersion(dfs: list[pd.DataFrame], baskets: list[Basket]):
    baskets_seq = Seq(baskets)
    data_weeks = Seq(dfs).map(lambda x: x.groupby('week').agg({'<OPEN>': 'first', '<CLOSE>': 'last'})).to_list()
    profits_sum = np.array([0, 0, 0, 0])
    for week in data_weeks[0].index:
        profits = np.array(baskets_seq.map(lambda x: x.calculate_profit(
            np.array(Seq(data_weeks).map(lambda y: y[week]['<OPEN>'])),
            np.array(Seq(data_weeks).map(lambda y: y[week]['<CLOSE>'])))))
        profits_sum += profits

        currency_data



def run():
    dfs = load_data.load().map(label_weeks).to_list()
    # for x in dfs[0]['<OPEN>'].index:
    #     print(x)
    baskets = get_baskets()



run()

