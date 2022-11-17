import numpy as np

from history_analyzer import calculate_matrixes, calculate_best_strategies
from information_price import run
from send import send

np.set_printoptions(linewidth=100000, suppress=True)
avg_profits_matrix, probabilities_matrix = calculate_matrixes()
print('Платежная матрица:')
print(avg_profits_matrix)
print('Матрица вероятностей:')
print(probabilities_matrix)

print('Лучшие стратегии по критериям:')
print('1) Вальда (максимина)')
print('2) Максимакса')
print('3) Гурвица (k = 0.25)')
print('4) Гурвица (k = 0.5)')
print('5) Гурвица (k = 0.75)')
print('6) Сэвиджа')
print('7) Байеса')
print(calculate_best_strategies(avg_profits_matrix, probabilities_matrix))

run(avg_profits_matrix, probabilities_matrix)

#send(2, payoff_matrix, probabilities_matrix)