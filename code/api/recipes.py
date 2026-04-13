from fastapi import APIRouter, HTTPException, Query, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from schemas import RecipePreview, RecipeFull
from services import recipe_service

# Создаем роутер с префиксом и тегом для удобства в Swagger (/docs)
router = APIRouter(prefix="/recipes", tags=["Recipes"])


# Вспомогательная функция, которая вытаскивает язык пользователя из кук браузера
def get_lang(request: Request):
    return request.cookies.get("preferred_language", "ru")


# 1. Ручка для получения случайных рецептов (для главной страницы)
@router.get("/random", response_model=list[RecipePreview])
async def get_random_dishes(request: Request, number: int = 3, db: Session = Depends(get_db)):
    lang = get_lang(request)
    # Передаем db, чтобы работал Fallback (кэш в базе данных), если API упадет
    return await recipe_service.search_random_recipe(db, number, lang=lang)


# 2. Ручка для поиска по названию С ФИЛЬТРАМИ (те самые "квадратики")
@router.get("/search", response_model=list[RecipePreview])
async def search_by_name(
        request: Request,
        query: str = Query(..., min_length=3),  # Обязательный поиск от 3-х символов
        diet: Optional[str] = None,  # Фильтр: vegan, vegetarian, ketogenic...
        recipe_type: Optional[str] = None,  # Фильтр: breakfast, main course, dessert...
        db: Session = Depends(get_db)
):
    lang = get_lang(request)
    # Бэкенд сам переведет запрос на английский, если введена кириллица
    return await recipe_service.search_recipe_by_name(db, query, diet=diet, recipe_type=recipe_type, lang=lang)


# 3. Ручка для поиска по ингредиентам (Твой "Холодильник")
@router.get("/by-ingredients", response_model=list[RecipePreview])
async def search_by_ingredients(request: Request, ingredients: str, db: Session = Depends(get_db)):
    lang = get_lang(request)
    return await recipe_service.search_by_ingredients(db, ingredients, lang=lang)


# 4. Ручка для получения полной информации о рецепте (Детальная страница)
@router.get("/{recipe_id}/info", response_model=RecipeFull)
async def get_info(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    lang = get_lang(request)
    # Пытаемся взять данные из API или из нашей таблицы-дублера RecipeCache
    res = await recipe_service.get_recipe_info(db, recipe_id, lang=lang)

    if not res:
        # Если рецепта нет ни в интернете, ни в нашей базе
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return res