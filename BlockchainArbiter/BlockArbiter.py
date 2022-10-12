import binascii
import sys

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from dateutil.parser import parse

sys.path.append("../Blockchain")
from Block import Block

import constants
import arbiter


class BlockArbiter(Block):
    def _sign_block(self, private_key: RSAPrivateKey = None):
        signature, str_timestamp = arbiter.sign_hash(self.hash())
        self.__str_timestamp = str_timestamp
        return signature

    def verify_block_signature(self, public_key: RSAPublicKey = None):
        return arbiter.verify(self.hash(), self.__str_timestamp, self._block_signature)

    @property
    def timestamp(self):
        return parse(self.__str_timestamp)

    @property
    def timestamp_str(self):
        return self.__str_timestamp

    def info(self):
        return f'Data: {self.data.decode(constants.encoding)}\n' f'Block number: {self.block_number}\n'\
               f'Previous hash: {binascii.hexlify(self.previous_hash).decode("utf-8")}\n'\
               f'Data signature: {binascii.hexlify(self.data_signature).decode("utf-8")}\n'\
               f'Block signature by arbiter: {binascii.hexlify(self.block_signature).decode("utf-8")}\n' \
               f'Block signature by arbiter timestamp: {self.timestamp}\n'

