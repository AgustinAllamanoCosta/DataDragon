import uuid
import datetime
from typing import List
from zkp.api.zkp import random_private_input
from subprocess import call

DEFAULT_CHAIN_LENGTH: int = 3
NODE_ID: str = str(uuid.uuid4())
KNOW_NODES: List[str] = []


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
        "know_nodes": KNOW_NODES
    }
