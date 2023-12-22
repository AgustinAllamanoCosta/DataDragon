
from src.api.service import Service
from fastapi import FastAPI
import uvicorn

api = FastAPI()
service = Service()

@api.get("/healthcheck/")
def read_root():
    return service.run_helath_check_test()

@api.get("/")
def node_data():
    return service.get_node_data()

@api.post("/prover")
async def proove_data():
    print("prover request ")

def run():
    uvicorn.run(api, host="0.0.0.0", port=80)