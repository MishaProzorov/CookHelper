from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from services import user_service as service
from auth import templates, security

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("head.html", {"request": request, "active": "home", "user": user})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("about.html", {"request": request, "active": "about", "user": user})

@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("search.html", {"request": request, "active": "search", "user": user})

@router.get("/help", response_class=HTMLResponse)
async def help(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("help.html", {"request": request, "active": "help", "user": user})

@router.get("/registration", response_class=HTMLResponse)
def registr(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("login.html", {"request": request, "active": "login", "user": user})

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    security.unset_access_cookies(response)
    return response

@router.get("/michelin", response_class=HTMLResponse)
async def michelin(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("michelin.html", {"request":request, "active": "michelin", "user": user})

