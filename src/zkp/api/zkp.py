#!/usr/bin/env python3
import json
from zkp.src.starkware.air.rescue.rescue_constants import PRIME
from zkp.src.starkware.main.rescue.rescue_end_to_end_test import generate_random_hex_witness_and_output

def random_private_input(chain_length:int):
    print('Generates random private and public inputs for the rescue prover.')

    witness_and_output = generate_random_hex_witness_and_output(PRIME, chain_length)
    witness, output = witness_and_output['witness'], witness_and_output['output']
    json.dump(
        {'witness': witness}
        ,open('/src/zkp/examples/rescue/rescue_private_input.json', 'w')
        , indent=4
    )
    json.dump(
        {'output': output, 'chain_length': chain_length}
        ,open('/src/zkp/examples/rescue/rescue_public_input.json', 'w')
        ,indent=4
    )
