import aiofiles
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from api.service import Service
from api.scan_service import ScanNode

app = FastAPI()
service = Service()
scan_service = ScanNode()

@app.get("/healthcheck/")
def read_root():
    return service.run_helath_check_test()

@app.get("/")
def node_data():
    return service.get_node_data()

@app.post("/proove")
async def proove_data(in_file: UploadFile=File(...)):
    async with aiofiles.open("/src/zkp/examples/ziggy/proof.json", 'wb') as out_file:
        while content := await in_file.read(1024):
            await out_file.write(content)
        return service.validate()
