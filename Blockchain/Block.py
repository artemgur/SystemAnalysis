from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.exceptions import InvalidSignature
import binascii

import constants


class Block:
    def __init__(self, data: str, signature_private_key: RSAPrivateKey, previous_block: 'Block | None'):
        self.__data = data.encode(constants.encoding)
        #self.test_data_str = data
        self.__block_number = previous_block.block_number + 1 if previous_block is not None else 0
        self.__previous_hash = previous_block.hash() if previous_block is not None else None
        self.__data_signature = self.__sign_data(signature_private_key)
        self._block_signature = self._sign_block(signature_private_key)

    def info(self):
        return f'Data: {self.__data.decode(constants.encoding)}\n' f'Block number: {self.__block_number}\n'\
               f'Previous hash: {binascii.hexlify(self.__previous_hash).decode("utf-8")}\n'\
               f'Data signature: {binascii.hexlify(self.__data_signature).decode("utf-8")}\n'\
               f'Block signature: {binascii.hexlify(self._block_signature).decode("utf-8")}\n'

    @property
    def data(self):
        return self.__data

    @property
    def data_signature(self):
        return self.__data_signature

    @property
    def block_signature(self):
        return self._block_signature

    @property
    def block_number(self):
        return self.__block_number

    @property
    def previous_hash(self):
        return self.__previous_hash

    def hash(self):
        data_to_hash = self._data_to_hash()
        hasher = hashes.Hash(constants.hash_function)
        hasher.update(data_to_hash)
        return hasher.finalize()

    def _data_to_hash(self):
        data_to_hash = self.__previous_hash + b'\n' if self.__previous_hash is not None else b''
        data_to_hash += self.__data
        data_to_hash += self.__data_signature
        return data_to_hash

    def __sign_data(self, private_key: RSAPrivateKey):
        return private_key.sign(self.__data,
                padding.PSS(mgf = padding.MGF1(constants.hash_function),salt_length = padding.PSS.MAX_LENGTH),
                constants.hash_function)

    def _sign_block(self, private_key: RSAPrivateKey):
        return private_key.sign(self.hash(),
                padding.PSS(mgf = padding.MGF1(constants.hash_function),salt_length = padding.PSS.MAX_LENGTH),
                utils.Prehashed(constants.hash_function))

    def verify_data_signature(self, public_key: RSAPublicKey):
        try:
            public_key.verify(self.__data_signature, self.__data,
                padding.PSS(mgf=padding.MGF1(constants.hash_function), salt_length=padding.PSS.MAX_LENGTH),
                constants.hash_function)
        except InvalidSignature:
            return False
        return True

    def verify_block_signature(self, public_key: RSAPublicKey):
        try:
            public_key.verify(self._block_signature, self.hash(),
                              padding.PSS(mgf=padding.MGF1(constants.hash_function), salt_length=padding.PSS.MAX_LENGTH),
                              utils.Prehashed(constants.hash_function))
        except InvalidSignature:
            return False
        return True

    def verify_signatures(self, public_key: RSAPublicKey):
        return self.verify_data_signature(public_key) and self.verify_block_signature(public_key)
