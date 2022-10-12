import json
import requests
from dateutil.parser import parse
import binascii

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.exceptions import InvalidSignature

import sys
sys.path.append("../Blockchain")
import constants


__public_key = None


# noinspection PyShadowingBuiltins
def sign_hash(hash: bytes):
    hash_str = binascii.hexlify(hash).decode('utf-8')
    response_text = requests.get('http://89.108.115.118/ts?digest=' + hash_str).text
    response_json = json.loads(response_text)
    if response_json['status'] != 0:
        raise Exception(response_json['statusString'])
    str_timestamp = response_json['timeStampToken']['ts']
    #timestamp = parse(str_timestamp)
    signature: str = response_json['timeStampToken']['signature']
    return binascii.unhexlify(signature), str_timestamp


def get_public_key():
    global __public_key

    if __public_key is None:
        response_text = requests.get('http://89.108.115.118/ts/public').text
        key = RSA.importKey(binascii.unhexlify(response_text))
        #with open('arbiter_public_key.pem', 'wb') as file:
        #    file.write(key.export_key(format='PEM'))

        __public_key = load_pem_public_key(key.export_key(format='PEM'))

    return __public_key


def verify(hash: bytes, str_timestamp: str, signature: bytes):
    signature_data = str_timestamp.encode('utf-8') + hash
    try:
        __public_key.verify(signature, signature_data,
                          padding.PSS(mgf=padding.MGF1(constants.hash_function), salt_length=padding.PSS.MAX_LENGTH),
                          constants.hash_function)
    except InvalidSignature:
        return False
    return True
