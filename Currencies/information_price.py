import numpy as np

from criterions import bayes_strategy_profit
from history_analyzer import calculate_matrixes


def transform_probabilities_matrix(probabilities_matrix):
    return (1 - probabilities_matrix) / 3


def get_equal_probabilities_matrix(shape):
    return np.full(shape, 1 / shape[1])


def bayes(values, probabilities):
    return (np.array(values) * np.array(probabilities)).sum()


# noinspection SpellCheckingInspection
def merge_probabilities_matrixes(matrixes, matrix_probabilities):
    result = np.zeros(matrixes[0].shape)
    for i in range(len(matrixes)):
        result += matrixes[i] * matrix_probabilities[i]
    return result


def rescale_probabilities(a, b):
    s = a + b
    if s == 0:
        return 0.5, 0.5
    return a / s, b / s


def known_states(avg_profits_matrix, probabilities_matrix):
    result_profits = []
    result_probabilities = []
    for i0 in range(probabilities_matrix.shape[1]):
        for i1 in range(probabilities_matrix.shape[1]):
            for i2 in range(probabilities_matrix.shape[1]):
                for i3 in range(probabilities_matrix.shape[1]):
                    result_profits.append(max(avg_profits_matrix[0, i0], avg_profits_matrix[1, i1], avg_profits_matrix[2, i2], avg_profits_matrix[3, i3], 0))
                    result_probabilities.append(probabilities_matrix[0, i0] * probabilities_matrix[1, i1] * probabilities_matrix[2, i2] * probabilities_matrix[3, i3])
    return (np.array(result_profits) * np.array(result_probabilities)).sum()


# noinspection SpellCheckingInspection
def known_most_risky_matrixes(matrix_probabilities):
    result = []
    for i in range(matrix_probabilities.shape[0]):
        new_matrix = np.empty_like(matrix_probabilities)
        new_matrix[i] = np.array([*rescale_probabilities(matrix_probabilities[i, 0], matrix_probabilities[i, 1]), 0, 0])
        for j in range(matrix_probabilities.shape[0]):
            if j != i:
                new_matrix[j] = np.array([0, 0, *rescale_probabilities(matrix_probabilities[i, 0], matrix_probabilities[i, 1])])
        result.append(new_matrix)
    return result


def run(avg_profits_matrix, probabilities_matrix):
    transformed_probabilities_matrix = transform_probabilities_matrix(probabilities_matrix)
    equal_probabilities_matrix = get_equal_probabilities_matrix(probabilities_matrix.shape)
    probabilities_merged = merge_probabilities_matrixes([probabilities_matrix,
                                                         transformed_probabilities_matrix,
                                                         equal_probabilities_matrix],
                                                        [1/3] * 4)

    merged_probabilities_profit = bayes_strategy_profit(avg_profits_matrix, probabilities_merged)[1]

    profit_1 = known_states(avg_profits_matrix, probabilities_merged)

    print('Максимальная сумма платы за информацию:')
    print('1) Какому состоянию природы будет соответствовать каждая сделка для каждой стратегии')
    print(profit_1 - merged_probabilities_profit)

    transformed_probabilities_profit = bayes_strategy_profit(avg_profits_matrix, transformed_probabilities_matrix)
    equal_probabilities_profit = bayes_strategy_profit(avg_profits_matrix, equal_probabilities_matrix)
    original_probabilities_profit = bayes_strategy_profit(avg_profits_matrix, probabilities_matrix)

    profits_2 = list(map(lambda x: bayes_strategy_profit(avg_profits_matrix, x)[1], known_most_risky_matrixes(transformed_probabilities_matrix)))
    profit_2 = bayes(profits_2, [1 / len(profits_2)] * len(profits_2))
    print('2) Какая из стратегий будет наиболее рискованной для Вашего набора данных')
    print(profit_2 - merged_probabilities_profit)

    profit_3 = bayes([transformed_probabilities_profit[1], equal_probabilities_profit[1], original_probabilities_profit[1]],
                     [1/3] * 3)
    print('3) Какая из версий оценки вероятностей является наиболее достоверной')
    print(profit_3 - merged_probabilities_profit)


