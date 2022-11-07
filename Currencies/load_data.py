import pandas as pd
from expression.collections import Seq

import constants


def load():
    return Seq(constants.currencies).map(lambda x: x + '.csv').map(lambda x: pd.read_csv(x))#.to_list()
