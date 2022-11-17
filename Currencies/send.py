import requests
import json

from constants import currencies


def send(strategy, payoff_matrix, probabilities_matrix):
    data = {'name': 'Гурьянов Артем Игоревич, 11-909', 'strategy': strategy}
    for i, currency in enumerate(currencies):
        data[f'currency{i + 1}'] = currency

    for i_strategy in range(payoff_matrix.shape[0]):
        for i_state in range(payoff_matrix.shape[1]):
            data[f'x{i_strategy + 1}{i_state + 1}'] = payoff_matrix[i_strategy, i_state]
            data[f'p{i_strategy + 1}{i_state + 1}'] = probabilities_matrix[i_strategy, i_state]

    data_json = json.dumps(data, ensure_ascii=False)
    print(data_json)

    response = requests.get('http://89.108.115.118/currency?value=' + data_json).text
    print(response)
