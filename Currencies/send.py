import requests


data = '{"name": "Гурьянов Артем Игоревич, 11-909", "currency1": "CNY", "currency2": "SGD", "currency3": "IDR", "currency4": "INR", "strategy": "2"}'
requests.get('http://89.108.115.118/curency?value=' + data)