import json
import hashlib
import requests
import binascii

import rsa


def get_last_data_str(json_str: str):
    data_str = '"data":'
    last_data_start_index = json_str.rfind(data_str) + len(data_str)
    last_data_end_index = json_str.find('}', last_data_start_index) + 1
    print('last data: ', json_str[last_data_start_index:last_data_end_index], '\n')
    return json_str[last_data_start_index:last_data_end_index]


def get_block(block_index):
    response_json_str = requests.get('http://89.108.115.118/nbc/chain').text
    response_json = json.loads(response_json_str)
    last_block = response_json[block_index]
    last_block['data'] = get_last_data_str(response_json_str)
    return last_block


def get_last_block():
    return get_block(-1)


def get_block_hash(block_index):
    last_block = get_block(block_index)
    data_to_hash = binascii.unhexlify(last_block['prevhash']) + last_block['data'].encode('utf-8') + last_block['ts'].encode('utf-8')# + binascii.unhexlify(last_block['signature'])
    hasher = hashlib.sha256()
    hasher.update(data_to_hash)
    return hasher.hexdigest()


def get_last_block_hash():
    return get_block_hash(-1)


def add_block(nn_results: str):
    nn_results_signature = rsa.sign_hex(nn_results)
    prev_hash = get_last_block_hash()
    block_dict = {'prevhash': prev_hash, 'data': '', 'signature': nn_results_signature}
    json_to_send = json.dumps(block_dict).replace('"data": ""', f'"data": {nn_results}')
    print(json_to_send)

    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    response = requests.post('http://89.108.115.118/nbc/newblock/', json=json_to_send, headers=headers)
    return response.text
