from fastapi import FastAPI
from api.service import do_ping, get_node_data, run_helath_check_test

app = FastAPI()

@app.get("/healthcheck/")
def read_root():
    return run_helath_check_test()

@app.get("/")
def node_data():
    return get_node_data()
