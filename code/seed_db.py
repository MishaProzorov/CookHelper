import asyncio
from database import session
from models import RecipeCache
from services.recipe_service import _make_request, translate_text


async def start_seeding():
    db = session()
    print("Загрузка 10 базовых рецептов для бесперебойной работы...")
    data = await _make_request("https://api.spoonacular.com/recipes/random", {"number": 10})
    if not data: return

    for r in data.get("recipes", []):
        if db.query(RecipeCache).filter(RecipeCache.id == r["id"]).first(): continue
        print(f"Сохраняю: {r['title']}")
        ingr = ", ".join([i.get("original", "") for i in r.get("extendedIngredients", [])])
        db.add(RecipeCache(
            id=r["id"], title_en=r["title"], title_ru=await translate_text(r["title"]),
            image=r.get("image"), ingredients_en=ingr, ingredients_ru=await translate_text(ingr),
            instructions_en=r.get("instructions"), instructions_ru=await translate_text(r.get("instructions", ""))
        ))
    db.commit()
    print("Готово!")


if __name__ == "__main__":
    asyncio.run(start_seeding())