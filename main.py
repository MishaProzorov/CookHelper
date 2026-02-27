from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get():
    return "Hellow word"

# @app.get("/item")
# def list():


@app.get("/")
def get():
    return "Hellow word"