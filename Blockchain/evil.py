import constants
from Block import Block


def change_block_data(block: Block, new_data: str):
    block._Block__data = new_data.encode(constants.encoding)

