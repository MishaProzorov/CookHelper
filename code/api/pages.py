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

@router.get("/reviews", response_class=HTMLResponse)
async def reviews(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("reviews.html", {"request":request, "active": "reviews", "user": user})

@router.get("/developers", response_class=HTMLResponse)
async def developers(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("developers.html", {"request":request, "active": "developers", "user": user})

@router.get("/techno", response_class=HTMLResponse)
async def techno(request: Request, db: Session = Depends(get_db)):
    user = await service.current_user(request, db)
    return templates.TemplateResponse("techno.html", {"request":request, "active": "techno", "user": user})



@router.get("/set-lang/{lang}")
async def set_language(lang: str, request: Request):
    target_lang = "ru" if lang == "ru" else "en"

    # Редирект на ту страницу, с которой пришел пользователь (или на главную)
    referer = request.headers.get("referer", "/")
    response = RedirectResponse(url=referer)

    # Ставим куку на 1 год
    response.set_cookie(key="preferred_language", value=target_lang, max_age=31536000)
    return response


# Добавь в api/pages.py

@router.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail_page(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    # 1. Получаем язык
    lang = request.cookies.get("preferred_language", "ru")

    # 2. Вызываем твой сервис (он сам решит: брать из API или из Базы)
    recipe = await service.get_recipe_info(db, recipe_id, lang=lang)

    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден в базе или в API")

    # 3. Отдаем HTML-страницу (пусть друг создаст файл recipe_info.html)
    return templates.TemplateResponse("recipe_info.html", {
        "request": request,
        "active": "search",
        "user": await service.current_user(request, db),
        "recipe": recipe  # Прокидываем объект RecipeFull со всеми данными
    })