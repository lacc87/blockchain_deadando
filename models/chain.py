from models.block import Block
from random import random

class Chain:
    def __init__(self):
        self.__number_of_zeros = 5
        self.__chain = []
        self.create_genesis()

    def get_last_block(self):
        return self.__chain[-1]

    def validate_old_block(self, block):
        found = False
        for b in self.__chain:
            if b.hash() == block and block.index == b.index:
                found = True
                break
        return found


    def validate_new_block(self, block):
        if self.get_last_block().index + 1 != block.index:
            return False
        if self.get_last_block().hash() != block.prev_hash:
            return False
        if not self.validate_proof_of_work(block):
            return False
        return True

    def add_new_block(self, block):
        if self.validate_new_block(block):
            self.__chain.append(block)

    def generate_proof_of_work(self, block):
        while not self.validate_proof_of_work(block):
            block.nonce = random()
        return block

    def create_new_block(self, tx):
        new_block = Block(self.get_last_block().hash(), 0, self.get_last_block().index + 1, tx.hash())
        return new_block

    def validate_proof_of_work(self, block):
        return block.hash()[:self.__number_of_zeros] == ''.join(['0' for _ in range(self.__number_of_zeros)])

    def create_genesis(self):
        genesis_block = Block('', 0, 1, '')
        genesis_block.created_at = 0
        self.__chain.append(genesis_block)