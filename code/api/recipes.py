from fastapi import APIRouter, HTTPException, Query, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db # Импортируем подключение к БД
from schemas import RecipePreview, RecipeFull
from services import recipe_service

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# Вспомогательная функция для получения языка из куки (оставили как было)
def get_lang(request: Request):
    return request.cookies.get("preferred_language", "ru")

# 1. Ручка для рандомных рецептов
@router.get("/random", response_model=list[RecipePreview])
async def get_random_dishes(request: Request, number: int = 3, db: Session = Depends(get_db)):
    lang = get_lang(request)
    # ВАЖНО: передаем db ПЕРВЫМ аргументом
    return await recipe_service.search_random_recipe(db, number, lang=lang)

# 2. Ручка для умного поиска
@router.get("/search", response_model=list[RecipePreview])
async def search_by_name(
    request: Request,
    query: str = Query(..., min_length=3),
    diet: Optional[str] = None,
    recipe_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    lang = get_lang(request)
    # ВАЖНО: передаем db ПЕРВЫМ аргументом
    return await recipe_service.search_recipe_by_name(db, query, lang=lang)

# 3. Ручка для поиска по ингредиентам
@router.get("/by-ingredients", response_model=list[RecipePreview])
async def search_by_ingredients(request: Request, ingredients: str, db: Session = Depends(get_db)):
    lang = get_lang(request)
    # ВАЖНО: передаем db ПЕРВЫМ аргументом
    return await recipe_service.search_by_ingredients(db, ingredients, lang=lang)

# 4. Ручка для детальной инфы по ID
@router.get("/{recipe_id}/info", response_model=RecipeFull)
async def get_info(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    lang = get_lang(request)
    # ВАЖНО: передаем db ПЕРВЫМ аргументом
    res = await recipe_service.get_recipe_info(db, recipe_id, lang=lang)
    if not res:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return res