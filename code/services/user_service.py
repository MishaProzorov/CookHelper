from fastapi import Request, HTTPException, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import User
from database import get_db
from auth import get_password_hashe, verify_password, security
from schemas import UserCreate


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


def get_user_by_gmail(db, gmail):
    return db.query(User).filter(User.gmail == gmail).first()


def creat_user(request: Request, gmail: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail == gmail).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким gmail уже зарегестрирован")

    hashed_pw = get_password_hashe(password)
    db_user = User(hashed_password=hashed_pw, gmail=gmail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = security.create_access_token(uid=str(db_user.id))
    response = RedirectResponse(url="/", status_code=302)
    security.set_access_cookies(token, response)
    return response


def login_user(request: Request, gmail: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail == gmail).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверная почта или пароль. Попробуйте еще раз")

    token = security.create_access_token(uid=str(db_user.id))
    response = RedirectResponse(url="/", status_code=302)
    security.set_access_cookies(token, response)
    return response


def return_user(db: Session = Depends(get_db)):
    return db.query(User).all()


def return_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Нет такого пользователя (id не существует)")
    return user


def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Невозможно удалить пользователя.")
    db.delete(user)
    db.commit()
    return user


def change_user(id: int, new: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователя с таким id не существует")
    user.hashed_password = new.password
    user.gmail = new.gmail
    db.commit()
    db.refresh(user)
    return user