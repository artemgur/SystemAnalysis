from math import sqrt


order_price = 1000
delivery_price = 1500
item_price = 100

daily_usage = 50  # v
daily_storage_price_per_item = 1  # s
#daily_loss_per_item = 0.01


task_literal = \
f'''Заводу по производству сока требутеся {daily_usage} кг апельсинов в день.
Стоимость оформления заказа – {order_price} р.
Стоимость доставки партии – {delivery_price} р.
Стоимость 1 кг апельсинов – {item_price} р.
Стоимость хранения 1 кг апельсинов 1 день – {daily_storage_price_per_item} р.
Нужно найти оптимальные: размер партии, время между заказами, средний объем запасов
'''
#Из 100 кг апельсинов в среднем в день портится {daily_loss_per_item * 100} кг.



def print_task():
    print(task_literal)


def solve():
    order_fixed_cost = order_price + delivery_price  # K
    #daily_storage_cost_per_item = daily_storage_price_per_item + daily_loss_per_item * item_price
    order_volume = sqrt(2 * order_fixed_cost * daily_usage / daily_storage_price_per_item)  # Q
    time_between_orders = order_volume / daily_usage
    average_storage = order_volume / 2
    print(f'Размер партии: {order_volume}')
    print(f'Время между заказами: {time_between_orders} дней')
    print(f'Средний объем запасов: {average_storage} кг')


print('Задача:')
print_task()
print('Результат:')
solve()