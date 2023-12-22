import base64
import datetime
import json
import traceback
import requests
import socketio
import random

from hashlib import sha256
from src.api.configuration import KNOW_NODES
from src.api.service import Service

sio = socketio.Client()
service = Service()
node_responses = {
   "true": 0,
   "false": 0
}

def validate_proof_file(node_responses):

  file = open("/src/zkp/examples/ziggy/proof.json", "rb")  
  nodes_to_use = KNOW_NODES
  print("node to use", nodes_to_use)
  while not len(nodes_to_use) == 0:
    index = random.randint(0,len(nodes_to_use)-1)
    node_url = nodes_to_use.pop(index)
    print("Sending proof to",node_url+"prover")
    node_response = requests.post(node_url+"prover",file)
    #if node_response["validation"] == True:
    #    node_responses["true"] += 1
    #else:
    #    node_responses["false"] += 1
  file.close()

def update_blockchain_or_not(node_responses):
    #if (node_responses["true"] / len(KNOW_NODES)) * 100 > 50:
    #  print("Todo update block chain")
    print("Todo update block chain")
    node_responses["true"]  = 0
    node_responses["false"] = 0

def start_back_task(task):
  sio.start_background_task(task)

def start_socket():
  sio.connect('http://datasource:5001')
  sio.wait()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def message(data):
    try:
      chunk:bytes = base64.b64decode(data['chunk'])
      if len(KNOW_NODES) != 0:
        timestamp = str(datetime.datetime.now())
        private_key = bytearray(random.getrandbits(8) for i in range(32 - len(chunk)))
        print("hash64 ", len(chunk + private_key))
        print("timestamp ", timestamp)
        service.generate_prover(chunk + private_key, timestamp)
        validate_proof_file(node_responses)
        update_blockchain_or_not(node_responses)
    except Exception as e:
      print("Error in chunk", e)
      print(traceback.format_exc())
   