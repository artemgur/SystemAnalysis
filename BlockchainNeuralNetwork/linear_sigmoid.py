import torch
from torch import nn


class LinearSigmoid(nn.Module):
    def __init__(self, linear_layer):
        super().__init__()
        self.linear = linear_layer

    def forward(self, x):
        return torch.sigmoid(self.linear(x))
