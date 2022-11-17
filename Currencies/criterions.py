def maximin(payoff_matrix):
    rows_min = payoff_matrix.min(axis=1)
    return rows_min.argmax()


def maximax(payoff_matrix):
    rows_max = payoff_matrix.max(axis=1)
    return rows_max.argmax()


def hurwicz(payoff_matrix, maximin_coef):
    rows = payoff_matrix.min(axis=1) * maximin_coef + payoff_matrix.max(axis=1) * (1 - maximin_coef)
    return rows.argmax()


def savage(payoff_matrix):
    columns_max = payoff_matrix.max(axis=0)
    matrix = columns_max[None, :] - payoff_matrix
    rows_max = matrix.max(axis=1)
    return rows_max.argmin()


def bayes_strategy_profit(payoff_matrix, probability_matrix):
    bayes_matrix = payoff_matrix * probability_matrix
    rows_bayes = bayes_matrix.sum(axis=1)
    return rows_bayes.argmax(), rows_bayes.max()


def bayes(payoff_matrix, probability_matrix):
    return bayes_strategy_profit(payoff_matrix, probability_matrix)[0]

