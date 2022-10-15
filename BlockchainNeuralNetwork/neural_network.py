import os
import torch
from torch import nn, optim
from torch.utils.data import DataLoader


#n_epochs = 10000
#learning_rate = 0.5


def train(x, y, n_epochs=10000, learning_rate=0.5):
    neural_network = nn.Sequential(
        nn.Linear(2, 2, bias=False),
        nn.Sigmoid(),
        nn.Linear(2, 3, bias=False),
        nn.Sigmoid(),
        nn.Linear(3, 1, bias=False),
        nn.Sigmoid()
    )

    loss_fn = nn.MSELoss(reduction='sum')
    optimizer = optim.SGD(neural_network.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5)

    for epoch in range(n_epochs):
        neural_network.train()

        prediction = neural_network(x)
        loss = loss_fn(y, prediction)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        scheduler.step(loss)
    with torch.no_grad():
        neural_network.eval()

        prediction = neural_network(x)
        loss = loss_fn(y, prediction)
        return loss.item(), list(map(lambda a: a.detach().numpy(), neural_network.parameters()))
