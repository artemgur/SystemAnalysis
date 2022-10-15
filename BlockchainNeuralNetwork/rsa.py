from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii


__public_filename = 'public_key.pem'
__private_filename = 'private_key.pem'

__public_key: RsaKey | None = None
__private_key: RsaKey | None = None


def load_key(filename):
    with open(filename, 'rb') as file:
        file_contents = file.read()
    return RSA.importKey(file_contents)


def public_key():
    global __public_key
    if __public_key is None:
        __public_key = load_key(__public_filename)
    return __public_key


def private_key():
    global __private_key
    if __private_key is None:
        __private_key = load_key(__private_filename)
    return __private_key


def public_key_hex():
    return binascii.hexlify(public_key().export_key('DER', pkcs=8)).decode('utf-8')


def sign(text_to_sign: str):
    hasher = SHA256.new()
    signer = pkcs1_15.new(private_key())
    hasher.update(text_to_sign.encode('utf-8'))
    return signer.sign(hasher)


def sign_hex(text_to_sign):
    return binascii.hexlify(sign(text_to_sign)).decode('utf-8')
