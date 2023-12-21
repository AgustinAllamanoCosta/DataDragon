
import random
from threading import Thread
from typing import List
import requests
import json
import datetime
from hashlib import sha256
import json
import websockets
from api.configuration import KNOW_NODES
from api.service import Service

class SocketClient(object):
    service: Service
    nodes_to_use: List[str] = []
    node_response = {
        "true": 0,
        "false": 0,
    }

    def __init__(self,service) -> None:
        self.service = service
        thread = Thread(target=self.start)
        thread.start()
  
    async def start(self):
      async with websockets.connect('ws://172.20.10.2:8080') as websocket:
          while True:
              try:
                chunk = await websocket.recv()
                if not chunk:
                    return
                chunk_from_json = json.load(chunk)
                print("Node chunk info ")
                hash64 = int.from_bytes(sha256(chunk_from_json["chunk"]).digest()[:8], 'little')
                timestamp = str(datetime.now())
                await self.service.generate_prover(hash64, timestamp)
                with open("/src/zkp/examples/ziggy/proof.json", "r") as f:
                  proof_data = json.load(f)

                self.nodes_to_use = KNOW_NODES
                while not len(self.nodes_to_use) == 0:
                    index = random.randint(0,len(self.nodes_to_use)-1)
                    node_url = self.nodes_to_use.pop(index)
                    node_response = requests.post(node_url,proof_data)
                    if node_response["validation"] == True:
                        self.node_response["true"] += 1
                    else:
                        self.node_response["false"] += 1

                if (self.node_response["true"] / len(KNOW_NODES)) * 100 > 50:
                    print("Todo update block chaim")
              except Exception as e:
                  print(e)