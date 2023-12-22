import os
import datetime
from time import sleep
from src.api.configuration import IP_ADDR, HOSTNAME, KNOW_NODES, NODE_ID, DEFAULT_CHAIN_LENGTH
from src.zkp.api.zkp import generate_ziggy_keys, random_private_input
from subprocess import call


class Service(object):

    def run_rescue_prover(self):

        executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_prover"
        cmd = [
            "--parameter_file",
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

    def run_rescue_validation(self):

        executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_verifier"
        cmd = [
            "--in_file",
            "/src/zkp/examples/rescue/proof.json",
            "--logtostderr"
        ]
        proc = call([executable] + cmd)
        os.remove('/src/zkp/examples/rescue/proof.json')
        return proc

    def run_helath_check_test(self):
        try:
            random_private_input(chain_length=DEFAULT_CHAIN_LENGTH)
            prover_response = self.run_rescue_prover()
            validation_response = self.run_rescue_validation()
            if prover_response > 0 or validation_response > 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False

    def get_node_data(self):
        is_healthy = self.run_helath_check_test()
        return {
            "id": NODE_ID,
            "is_healthy": is_healthy,
            "date": datetime.datetime.now(),
            "know_nodes": KNOW_NODES,
            "IP": IP_ADDR,
            "HostName": HOSTNAME
        }

    def validate(
        self
    ):
        print("validate file")
        executable = "/src/zkp/build/Release/src/starkware/main/ziggy/ziggy_verifier"
        cmd = [
            "--in_file",
            "/src/zkp/examples/ziggy/proof-receive.json",
            "--logtostderr"
        ]
        call([executable] + cmd)
        sleep(5)

    def generate_prover(
        self,
        private_key:str,
        message:str
    ):
        print("generating keys")
        generate_ziggy_keys(private_key,message)

        print("generating prover file")
        executable = "/src/zkp/build/Release/src/starkware/main/ziggy/ziggy_prover"
        cmd = [
            "--parameter_file",
            "/src/zkp/examples/ziggy/ziggy_params.json",
            "--prover_config_file",
            "/src/zkp/examples/ziggy/ziggy_prover_config.json",
            "--public_input_file",
            "/src/zkp/examples/ziggy/ziggy_public_input.json",
            "--private_input_file",
            "/src/zkp/examples/ziggy/ziggy_private_input.json",
            "--out_file",
            "/src/zkp/examples/ziggy/proof.json",
            "--logtostderr"
        ]
        call([executable] + cmd)