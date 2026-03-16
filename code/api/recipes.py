from fastapi import APIRouter, HTTPException, Query
from services import recipe_service # Твой движок

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# 1. Ручка для рандомных рецептов
@router.get("/random")
async def get_random_dishes(number: int = 3):
    # ТВОЯ ЛОГИКА: вызываем асинхронный сервис
    res = await recipe_service.search_random_recipe(number)
    if not res:
        raise HTTPException(status_code=404, detail="Не удалось получить рецепты")
    return res

# 2. Ручка для поиска по названию
@router.get("/search")
async def search_by_name(query: str = Query(..., min_length=3)):
    # ТВОЯ ЛОГИКА: Query(...) делает параметр обязательным
    res = await recipe_service.search_recipe_by_name(query)
    return res

# 3. Ручка для поиска по ингредиентам
@router.get("/by-ingredients")
async def search_by_ingredients(ingredients: str):
    # Ожидаем строку типа "apple,milk"
    res = await recipe_service.search_by_ingredients(ingredients)
    return res

# 4. Ручка для детальной инфы по ID
@router.get("/{recipe_id}/info")
async def get_info(recipe_id: int):
    res = await recipe_service.get_recipe_info(recipe_id)
    if not res:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return res