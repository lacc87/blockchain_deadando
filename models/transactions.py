import time
import hashlib
import json

class Transaction:
    def __init__(self, from_id, to_id, coin):
        self.from_id = from_id
        self.to_id = to_id
        self.coin = coin
        self.created_at = time.time()

    def as_json(self):
        return json.dumps(self.__dict__)

    def hash(self):
        sha = hashlib.sha256()
        sha.update(self.as_json().encode('utf-8'))
        return sha.hexdigest()
