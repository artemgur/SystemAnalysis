import numpy as np
import torch
from expression.collections import Seq


def load_data(filename: str):
    with open(filename, 'r') as file:
        data = list(Seq(file.read().split('\n')).filter(lambda a: a)
                    .map(lambda a: list(Seq(a.split(';')).map(lambda b: float(b)))))
    x = np.array(list(Seq(data).map(lambda a: a[:2])))
    y = np.array(list(Seq(data).map(lambda a: a[-1:])))
    return torch.from_numpy(x).float(), torch.from_numpy(y).float()
