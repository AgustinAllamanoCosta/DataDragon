
from fastapi import FastAPI, File, UploadFile
from api.service import Service
from api.scan_service import ScanNode
from api.socket_client import SocketClient

app = FastAPI()
service = Service()
scan_service = ScanNode()
#socker_service = SocketClient(service)

@app.get("/healthcheck/")
def read_root():
    return service.run_helath_check_test()

@app.get("/")
def node_data():
    return service.get_node_data()

@app.post("/prove")
async def proove_data(in_file: UploadFile=File(...)):
    print(in_file)
    # proof_receive_path = "/src/zkp/examples/ziggy/proof-receive.json"
    # async with aiofiles.open(proof_receive_path, 'wb') as out_file:
    #     while content in await in_file.read(1024):
    #         await out_file.write(content)
    #     validation = service.validate()
    #     os.remove(proof_receive_path) 
    #     return validation
