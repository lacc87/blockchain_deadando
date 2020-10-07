import time
import hashlib
import json

class Block:
    def __init__(self, prev_hash, nonce, index, tx_root):
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.index = index
        self.tx_root = tx_root
        self.created_at = time.time()

    def as_json(self):
        return json.dumps(self.__dict__)

    def hash(self):
        sha = hashlib.sha256()
        sha.update(self.as_json().encode('utf-8'))
        return sha.hexdigest()
