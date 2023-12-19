from fastapi import FastAPI
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

