from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends 
from models import  User
import os
from database import engine, session, Base
from schemas import UserClass, UserCreate
from fastapi.staticfiles import StaticFiles
from auth import get_password_hashe, verify_password
from fastapi import Form
from authx import AuthX, AuthXConfig

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
Base.metadata.create_all(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

async def current_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("my_token")
        if not token:
            return None

        payload = security._decode_token(token)
        user_id = payload.sub
        return db.query(User).filter(User.id == int(user_id)).first()
    except:
        return None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = await current_user(request, db)
    return templates.TemplateResponse("head.html", {"request": request, "active": "home", "user": user})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_db)):
    user = await current_user(request, db)
    return templates.TemplateResponse("about.html", {"request": request, "active": "about", "user": user})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, db: Session = Depends(get_db)):
    user = await current_user(request, db)
    return templates.TemplateResponse("search.html", {"request": request, "active": "search", "user": user})

@app.get("/help", response_class=HTMLResponse)
async def help(request: Request, db: Session = Depends(get_db)):
    user = await current_user(request, db)
    return templates.TemplateResponse("help.html", {"request": request, "active": "help", "user": user})


@app.post("/registration")
def creat_user(request: Request, gmail: str = Form(...), password: str = Form(...),  db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail == gmail).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким gmail уже зарегестрирован")
    
    hashed_pw = get_password_hashe(password)
    
    db_user = User(    
        hashed_password = hashed_pw, 
        gmail = gmail
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = security.create_access_token(uid=str(db_user.id))

    response = RedirectResponse(url="/", status_code = 302)
    security.set_access_cookies(token, response)
    return response

@app.post("/login")
def login_user(request: Request, gmail: str = Form(...), password: str = Form(...),  db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail == gmail).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверная почта или пароль. Попробуйте еще раз")
    token = security.create_access_token(uid=str(db_user.id))
    response = RedirectResponse(url="/", status_code = 302)
    security.set_access_cookies(token, response)
    return response

@app.get("/registration", response_class=HTMLResponse)
def registr(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    user = await current_user(request, db)
    return templates.TemplateResponse("login.html", {"request": request, "active": "login", "user": user})

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    security.unset_access_cookies(response)
    return response

# @app.get("/registration/", response_model=list[UserClass])
# def return_user(db: Session=Depends(get_db)):
#     users = db.query(User).all()
#     return users


# @app.get("/registration/{id}", response_model=UserClass)
# def return_one_user(id: int, db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.id == id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail = "Нет такого пользователя (id не существует)")
#     return user


# @app.delete("/registration/{id}", response_model=UserClass)
# def delete_user(id: int, db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.id == id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="Невозможно удалить пользователя.")
#     db.delete(user)
#     db.commit()
#     return user


# @app.put("/registration/{id}",response_model=UserClass)
# def change_user(id: int, new: UserCreate, db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.id == id).first()
#     if user is None:
#         raise HTTPException(
#             status_code=404, 
#             detail = "Пользователя с таким id не существует"
#         )
#     user.hashed_password = new.hashed_password
#     user.gmail = new.gmail
#     db.commit()
#     db.refresh(user)
#     return user



#почитать про Response, Jinja, html, разобрать подробнее что да как
#подключение и работа с базой данных