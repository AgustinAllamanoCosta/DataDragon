
import json
import os
from src.api.service import Service
from fastapi import FastAPI, File, UploadFile
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
async def proove_data(file: UploadFile = File(...)):
    file_content = await file.read()
    file_path = '/src/zkp/examples/ziggy/proof-receive.json'
    try:        
        if os.path.exists(file_path):
            os.remove(file_path)
        new_file = open(file_path, "xb")
        new_file.write(file_content)
        new_file.close()
        service.validate()
        return {"validation":True}
    except Exception as e:
        print("Prover erorr ",e)
        return {"validation":False}

def run():
    uvicorn.run(api, host="0.0.0.0", port=80)