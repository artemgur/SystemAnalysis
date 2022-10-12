from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import jsonpickle

from Block import Block
import utilities

class Blockchain:
    def __init__(self, block_list: list[Block], filename: str, block_type: type):
        self.__block_list = block_list
        self.__filename = filename
        self.__block_type = block_type

    @classmethod
    def create(cls, filename: str):
        return cls([],  filename, Block)

    @classmethod
    def load_from_file(cls, filename: str):
        blockchain = cls.create(filename)
        with open(filename, 'r') as file:
            for line in utilities.readlines(file):
                block = jsonpickle.decode(line)
                blockchain.__block_list.append(block)
        return blockchain

    @property
    def filename(self):
        return self.__filename

    def add_block(self, block_data: str, signature_private_key: RSAPrivateKey):
        if len(self.__block_list) == 0:
            self.__block_list.append(self.__block_type(block_data, signature_private_key, None))
        else:
            self.__block_list.append(self.__block_type(block_data, signature_private_key, self.__block_list[-1]))
        with open(self.__filename, 'a') as file:
            file.write(jsonpickle.encode(self.__block_list[-1]))
            file.write('\n')

    def __getitem__(self, item):
        return self.__block_list[item]

    def __len__(self):
        return len(self.__block_list)

    def verify_hashes(self, first_block = 0, last_block = None):
        if last_block is None:
            last_block = len(self) - 1
        blocks_to_verify = utilities.slice_closed(self.__block_list, first_block, last_block)
        result = True
        for i in utilities.range_closed(len(blocks_to_verify) - 1, 1, -1):
            if blocks_to_verify[i].previous_hash != blocks_to_verify[i - 1].hash():
                result = False
                break
        return result

    def verify_signatures(self, public_key: RSAPublicKey, first_block = 0, last_block = None):
        if last_block is None:
            last_block = len(self) - 1
        blocks_to_verify = self.__block_list[first_block:last_block - 1]
        result = True
        for i in utilities.range_closed(len(blocks_to_verify) - 1, 0, -1):
            if not blocks_to_verify[i].verify_signatures(public_key):
                result = False
                break
        return result

    def verify(self, public_key: RSAPublicKey, first_block = 0, last_block = None):
        return self.verify_hashes(first_block, last_block) and self.verify_signatures(public_key, first_block, last_block)
