import datetime
from api.configuration import IP_ADDR, HOSTNAME, KNOW_NODES, NODE_ID, DEFAULT_CHAIN_LENGTH
from zkp.api.zkp import random_private_input
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

    def validate(self):
        executable = "/src/zkp/build/Release/src/starkware/main/ziggy/ziggy_verifier"
        cmd = [
            "--in_file",
            "/src/zkp/examples/ziggy/proof.json",
            "--logtostderr"
        ]        
        return call([executable] + cmd)

    def generate_prover(
            self,
            private_key:str,
            message:str
        ):
        executable = "/src/zkp/examples/ziggy/generate_keys.py"
        cmd = [
            f"--private_key=[{0}]".format(private_key),
            f"--message=[{0}]".format(message)
        ]        
        call([executable] + cmd)

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
        proc = call([executable] + cmd)
        return proc
