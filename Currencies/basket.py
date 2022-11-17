from typing import Tuple

import numpy as np
from expression.collections import Seq


_basket_size = 1_000_000
_basket_ratios = [(0.1, 0.15, 0.15, 0.6), (0.3, 0.3, 0.3, 0.1), (0.6, 0.1, 0.1, 0.2), (0.35, 0.35, 0.15, 0.25)]
_basket_tuple = Tuple[float, float, float, float]


class Basket:
    def __init__(self, basket_ratio: _basket_tuple):
        self._basket_ratio = np.array(basket_ratio)
        self._basket_values = self._basket_ratio * _basket_size


    def calculate_profit(self, buy_prices: np.ndarray, sell_prices: np.ndarray):
        #buy_prices_arr = np.array(buy_prices)
        #sell_prices_arr = np.array(sell_prices)

        price_ratio = sell_prices / buy_prices
        new_prices = self._basket_values * price_ratio
        return (new_prices - self._basket_values).sum()

    # currency_prices: строки – дни, столбцы – валюты
    def calculate_risk(self, currency_prices: np.ndarray):
        basket_prices: np.ndarray = (currency_prices * self._basket_ratio).sum(axis=1)
        return basket_prices.var()


def get_baskets():
    return Seq(_basket_ratios).map(Basket)