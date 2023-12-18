
from zkp.api.zkp import random_private_input
import subprocess

DEFAULT_CHAIN_LENGTH: int = 3

def run_helath_check_test():

    random_private_input(chain_length=DEFAULT_CHAIN_LENGTH)

    proc = subprocess.Popen(r"build/Release/src/starkware/main/rescue/rescue_prover \
        --parameter_file examples/rescue/rescue_params.json \
        --prover_config_file examples/rescue/rescue_prover_config.json \
        --public_input_file examples/rescue/rescue_public_input.json \
        --private_input_file examples/rescue/rescue_private_input.json \
        --out_file examples/rescue/proof.json \
        --logtostderr")
    outs, errs = proc.communicate(timeout=15)
    print(outs)

    proc = subprocess.Popen(r"build/Release/src/starkware/main/rescue/rescue_verifier \
        --in_file examples/rescue/proof.json \
        --logtostderr")
    outs, errs = proc.communicate(timeout=15)
    print(outs)