
import json
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
async def proove_data(request: UploadFile = File(...)):
    file_content = await request.read()
    print("waka ", file_content)
    with open('/src/zkp/examples/ziggy/proof-receive.json', "wb")  as new_file:
        new_file.write(file_content)
    service.validate()
    return {"validation":True}

def run():
    uvicorn.run(api, host="0.0.0.0", port=80)