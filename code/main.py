from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Depends 
from models import  User
import os
from database import engine, session, Base
from schemas import UserClass, UserCreate
from fastapi.staticfiles import StaticFiles

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("head.html", {"request": request})

@app.get("/registration", response_class=HTMLResponse)
def registr(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/registration/", response_model=UserClass)
def creat_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name = user.name, 
        age = user.age, 
        password = user.password, 
        gmail = user.gmail
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/registration/", response_model=list[UserClass])
def return_user(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/registration/{id}", response_model=UserClass)
def return_one_user(id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail = "Нет такого пользователя (id не существует)")
    return user


@app.delete("/registration/{id}", response_model=UserClass)
def delete_user(id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Невозможно удалить пользователя.")
    db.delete(user)
    db.commit()
    return user


@app.put("/registration/{id}",response_model=UserClass)
def change_user(id: int, new: UserCreate, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail = "Пользователя с таким id не существует"
        )
    user.name = new.name
    user.age = new.age
    user.password = new.password
    user.gmail = new.gmail
    db.commit()
    db.refresh(user)
    return user




# @app.get("/")
# def get():
#     return "Hellow"