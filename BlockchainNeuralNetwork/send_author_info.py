import json

import requests

import rsa


__author_name = 'Гурьянов Артем Игоревич, 11-909'


def send():
    dict_to_send = {'autor': __author_name, 'sign': rsa.sign_hex(__author_name), 'publickey': rsa.public_key_hex()}

    json_to_send = json.dumps(dict_to_send)

    response = requests.post('http://89.108.115.118/nbc/autor', json=json_to_send)
    return response.text
