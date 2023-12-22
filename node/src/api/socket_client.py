import base64
from copy import *
import datetime
import json
import traceback
import requests
import socketio
import random

from hashlib import sha256
from src.blockchain.blockchain import Blockchain
from src.api.configuration import KNOW_NODES
from src.api.service import Service

sio = socketio.Client()
service = Service()

blockchain = Blockchain()

def validate_proof_file(node_responses):
  file = open("/src/zkp/examples/ziggy/proof.json", "rb")  
  nodes_to_use = copy(KNOW_NODES)
  while not len(nodes_to_use) == 0:
    index = random.randint(0,len(nodes_to_use)-1)
    node_url = nodes_to_use.pop(index)
    files = {"file": file}
    node_response = requests.post(node_url+"prover", files=files)
    print("proveer response", node_response.json())
    if node_response.json()["validation"] == True:
        print("valid plus one")
        node_responses["true"] += 1
    else:
        print("invalid plus one")
        node_responses["false"] += 1
  file.close()

def update_blockchain_or_not(node_responses,data):
    
    if ( node_responses["true"] != 0 and node_responses["true"] / len(KNOW_NODES)) * 100 > 50:
      blockchain.addBlock(data["chunk"], data["index"], data["filename"])
      jsonBlockchain = json.dumps(Blockchain.toDictionary(blockchain.chain))
      print('blockchain_data', json.dumps(Blockchain.toDictionary(blockchain.chain)))
    else:
      print("False 51%")

def start_back_task(task):
  sio.start_background_task(task)

def start_socket():
  sio.connect('http://datasource:5002')
  sio.wait()

@sio.event
def connect():
    print('connection established')
    jsonBlockchain = json.dumps(Blockchain.toDictionary(blockchain.chain))
    print("jsonBlockchain", jsonBlockchain)
    sio.emit('blockchain_data', jsonBlockchain)

@sio.on("get_blockchain_data")
def getBlockchain():
    jsonBlockchain = json.dumps(Blockchain.toDictionary(blockchain.chain))
    sio.emit('blockchain_data', jsonBlockchain)

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def message(data):
    try:
      chunk:bytes = base64.b64decode(data['chunk'])
      node_responses = {
        "true": 0,
        "false": 0
      }
      if len(KNOW_NODES) != 0:
        timestamp = str(datetime.datetime.now())
        private_key = bytearray(random.getrandbits(8) for i in range(32 - len(chunk)))
        service.generate_prover(chunk + private_key, timestamp)
        validate_proof_file(node_responses)
        update_blockchain_or_not(node_responses,data)
      else:
         print("Not enough nodes")
    except Exception as e:
      print("Error in chunk", e)
      print(traceback.format_exc())
   