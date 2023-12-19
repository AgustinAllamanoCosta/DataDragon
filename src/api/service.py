import json
import uuid
import socket
import datetime
from typing import List
from zkp.api.zkp import random_private_input
from subprocess import call 
from time import sleep
from threading import Thread
import requests


DEFAULT_CHAIN_LENGTH: int = 3
NODE_ID: str = str(uuid.uuid4())
KNOW_NODES: List[str] = []
HOSTNAME = socket.gethostname()
IP_ADDR = socket.gethostbyname(HOSTNAME)


def run_rescue_prover():

    executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_prover"
    cmd = ["--parameter_file",
           "/src/zkp/examples/rescue/rescue_params.json",
           "--prover_config_file",
           "/src/zkp/examples/rescue/rescue_prover_config.json",
           "--public_input_file",
           "/src/zkp/examples/rescue/rescue_public_input.json",
           "--private_input_file",
           "/src/zkp/examples/rescue/rescue_private_input.json",
           "--out_file",
           "/src/zkp/examples/rescue/proof.json",
           "--logtostderr"
    ]
    proc = call([executable] + cmd)
    return proc

def run_rescue_validation():

    executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_verifier"
    cmd = [
        "--in_file",
        "/src/zkp/examples/rescue/proof.json",
        "--logtostderr"
    ]
    proc = call([executable] + cmd)
    return proc

def run_helath_check_test():
    try:
        random_private_input(chain_length=DEFAULT_CHAIN_LENGTH)
        prover_response = run_rescue_prover()
        validation_response = run_rescue_validation()
        if prover_response > 0 or validation_response > 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False

def get_node_data():
    is_healthy = run_helath_check_test()
    return {
        "id": NODE_ID,
        "is_healthy": is_healthy,
        "date": datetime.datetime.now(),
        "know_nodes": KNOW_NODES,
        "IP": IP_ADDR,
        "HostName": HOSTNAME
    }

def do_ping():
    blocks = IP_ADDR.split('.')
    while True:
        sleep(1)
        for new_block in range(1,254):

            ip_to_ping: str = '{0}.{1}.{2}.{3}'.format(blocks[0],blocks[1],blocks[2],new_block)
            if ip_to_ping != IP_ADDR:

                url = 'http://{0}:80/'.format(ip_to_ping)
                response = requests.get(url,timeout=5)
                json_response = json.loads(response.text)

                if not url in KNOW_NODES and response.status_code == 200:
                    KNOW_NODES.append(url)

thread = Thread(target=do_ping)

thread.start()
