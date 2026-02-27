from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get():
    return "Hellow"

@app.get("/")
def get():
    return "Hellow"