import sys

sys.path.append("../Blockchain")
from BlockArbiter import BlockArbiter
from Blockchain import Blockchain


class BlockchainArbiter(Blockchain):
    @classmethod
    def create(cls, filename: str):
        return cls([],  filename, BlockArbiter)
