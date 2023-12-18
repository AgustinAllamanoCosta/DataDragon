from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck/")
def read_root():
    return {"Hello": "World"}
