from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return ("Главная страница")


        
