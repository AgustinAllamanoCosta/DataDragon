from zkp.api.zkp import random_private_input
import subprocess

DEFAULT_CHAIN_LENGTH: int = 3

def run_rescue_prover():

    executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_prover"
    cmd = "--parameter_file src/zkp/examples/rescue/rescue_params.json \
        --prover_config_file src/zkp/examples/rescue/rescue_prover_config.json \
        --public_input_file src/zkp/examples/rescue/rescue_public_input.json \
        --private_input_file src/zkp/examples/rescue/rescue_private_input.json \
        --out_file src/zkp/examples/rescue/proof.json \
        --logtostderr"
    run_process(executable,cmd)

def run_rescue_validation():

    executable = "/src/zkp/build/Release/src/starkware/main/rescue/rescue_verifie"
    cmd = "--in_file src/zkp/examples/rescue/proof.json \
        --logtostderr"
    run_process(executable,cmd)

def run_process(executable,cmd):

    proc = subprocess.Popen(executable=executable,args=cmd,shell=True)
    outs, errs = proc.communicate(timeout=15)
    print("out puts",outs)
    print("errors ",errs)

def run_helath_check_test():

    random_private_input(chain_length=DEFAULT_CHAIN_LENGTH)
    run_rescue_prover()
    run_rescue_validation()