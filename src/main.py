from fastapi import FastAPI
from api.service import run_helath_check_test
from api.service import get_node_data

app = FastAPI()

@app.get("/healthcheck/")
def read_root():
    return run_helath_check_test()

@app.get("/")
def node_data():
    return get_node_data()
