from models.chain import Chain
from models.block import Block
from models.transactions import Transaction
import json
import socket, time
import threading
from random import random
import os

time.sleep(2)

print("Miner")

chain = Chain()

my_ip = socket.gethostbyname(socket.gethostname())
my_name = ""
other_nodes = [
    {"host": "blockchain_deadando_miner_1", 'ip': ''},
    {"host": "blockchain_deadando_miner_2", 'ip': ''},
    {"host": "blockchain_deadando_miner_3", 'ip': ''},
    {"host": "blockchain_deadando_miner_4", 'ip': ''},
    {"host": "blockchain_deadando_miner_5", 'ip': ''}]
for n in other_nodes:
    n["ip"] = socket.gethostbyname(n['host'])
    if my_ip == n["ip"]:
        my_name = n['host']

class FindBlockThread:
    def __init__(self):
        self.__running = True
        self.block_found = False

    def create_block(self, tx):
        self.block = chain.create_new_block(tx)

    def terminate(self):
        self.__running = False

    def run(self):
        print("New Block finding started...")
        while not chain.validate_proof_of_work(self.block):
            if not self.__running:
                break
            self.block.nonce = random()
        if not self.__running:
            return
        self.block_found = True
        valids = []
        valid = 0
        print("New Block found...")
        for node in other_nodes:
            if node['host'] == my_name:
                valid = valid + 1
                continue
            s = socket.socket()
            host = node['host']
            port = 5000
            s.connect((host, port))
            s.sendall(bytes(json.dumps(self.block.__dict__), encoding="utf-8"))
            data = s.recv(1024 * 128).decode('utf-8')
            print(data)
            valid_json = json.loads(data)
            valids.append(valid_json)
            if valid_json['valid']:
                valid = valid + 1
            s.close()

        if valid > 2:
            chain.add_new_block(self.block)
        else:
            for v1 in valids:
                cnt = 0
                net_block = None
                for v2 in valids:
                    if v1['last_valid_block']['prev_hash'] == v2['last_valid_block']['prev_hash'] and v1['last_valid_block']['nonce'] == v2['last_valid_block']['nonce'] and v1['last_valid_block']['created_at'] == v2['last_valid_block']['created_at'] and v1['last_valid_block']['tx_root'] == v2['last_valid_block']['tx_root'] and v1['last_valid_block']['index'] == v2['last_valid_block']['index']:
                        cnt = cnt + 1
                    if cnt == 3:
                        net_block = Block(v1['last_valid_block']['prev_hash'],
                                          v1['last_valid_block']['nonce'],
                                          v1['last_valid_block']['index'],
                                          v1['last_valid_block']['tx_root'])
                        net_block.created_at = v1['last_valid_block']['created_at']
            if net_block and chain.validate_new_block(net_block):
                chain.add_new_block(net_block)
            else:
                # TODO replace chain
                print('__not valid__')


findblock = FindBlockThread()
x = False
print('Mining started')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 5000))
serversocket.listen(10)

findblock.create_block(Transaction(0, my_name, 1))
x = threading.Thread(target=findblock.run, args=())
x.start()

while True:
    (clientsocket, address) = serversocket.accept()
    print("New connection")
    with clientsocket:
        print('Connected by', address)
        while True:
            data = clientsocket.recv(1024 * 128).decode('utf-8')
            if not data:
                break
            block_json = json.loads(data)
            net_block = Block(block_json['prev_hash'], block_json['nonce'], block_json['index'], block_json['tx_root'])
            net_block.created_at = block_json['created_at']
            print(block_json)
            if chain.validate_new_block(net_block):
                valid = { 'valid': True}
                clientsocket.sendall(bytes(json.dumps(valid), encoding="utf-8"))
                print("BLOCK FROM NETWORK IS VALID")
                findblock.terminate()
                chain.add_new_block(net_block)

                findblock = FindBlockThread()
                findblock.create_block(Transaction(0, my_name, 1))
                x = threading.Thread(target=findblock.run, args=())
                x.start()
            else:
                valid = {'valid': False, 'last_valid_block': json.loads(chain.get_last_block().as_json())}
                clientsocket.sendall(bytes(json.dumps(valid), encoding="utf-8"))
                print("BLOCK FROM NETWORK IS NOT VALID")
        if not x.is_alive():
            findblock = FindBlockThread()
            findblock.create_block(Transaction(0, my_name, 1))
            x = threading.Thread(target=findblock.run, args=())
            x.start()

#while True:
 #   (clientsocket, address) = serversocket.accept()
  #  with clientsocket:
   #     print('Connected by', address)
    #    while True:
     #       data = clientsocket.recv(1024 * 128)
      #      if not data:
       #         break
        #    clientsocket.sendall(data)


print('Mining ended')