from fastapi import FastAPI
from api.service import run_helath_check_test

app = FastAPI()

@app.get("/healthcheck/")
def read_root():
    return run_helath_check_test()