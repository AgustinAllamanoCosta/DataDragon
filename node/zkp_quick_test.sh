PYTHONPATH=src examples/rescue/random_private_input.py --chain_length=3

build/Release/src/starkware/main/rescue/rescue_prover \
    --parameter_file examples/rescue/rescue_params.json \
    --prover_config_file examples/rescue/rescue_prover_config.json \
    --public_input_file examples/rescue/rescue_public_input.json \
    --private_input_file examples/rescue/rescue_private_input.json \
    --out_file examples/rescue/proof.json \
    --logtostderr

build/Release/src/starkware/main/rescue/rescue_verifier \
    --in_file examples/rescue/proof.json \
    --logtostderr
