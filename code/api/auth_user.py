from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from services import user_service as service
from database import get_db

router = APIRouter()

@router.post("/registration")
async def creat_user(
    request: Request,
    gmail: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db)
):
    try:
        return service.creat_user(request, gmail, password, db)
    except Exception as e:
        error_msg = str(e.detail) if hasattr(e, 'detail') else "Ошибка регистрации"
        return RedirectResponse(url=f"/registration?error={error_msg}", status_code=302)

@router.post("/login")
async def login_user(
    request: Request,
    gmail: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db)
):
    try:
        return service.login_user(request, gmail, password, db)
    except Exception as e:
        error_msg = str(e.detail) if hasattr(e, 'detail') else "Ошибка входа"
        return RedirectResponse(url=f"/login?error={error_msg}", status_code=302)