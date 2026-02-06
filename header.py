from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return ("Главная страница")

@app.get("/food")
def foodweb():
    return ("Страница о еде")