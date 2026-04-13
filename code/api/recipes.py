import httpx, asyncio, os, re
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from deep_translator import GoogleTranslator
from schemas import RecipePreview, RecipeFull
from models import RecipeCache
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.spoonacular.com/recipes"
raw_keys = os.getenv("SPOON_API_KEYS") or os.getenv("SPOON_API_KEY")
API_KEYS = [k.strip() for k in raw_keys.split(",")] if raw_keys else []
current_key_index = 0

async def translate_text(text: str, target: str = 'ru'):
    if not text or text == "Нет данных": return text
    try:
        return await asyncio.to_thread(GoogleTranslator(source='auto', target=target).translate, text)
    except: return text

async def _make_request(url: str, params: dict):
    global current_key_index
    if not API_KEYS: return None
    for _ in range(len(API_KEYS)):
        params["apiKey"] = API_KEYS[current_key_index]
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 402:
                    current_key_index = (current_key_index + 1) % len(API_KEYS)
                    continue
                return response.json() if response.status_code == 200 else None
            except: return None
    return None

async def search_random_recipe(db: Session, number: int = 3, lang: str = "ru"):
    data = await _make_request(f"{BASE_URL}/random", {"number": number})
    if data:
        results = []
        for r in data.get("recipes", []):
            title = await translate_text(r["title"]) if lang == "ru" else r["title"]
            results.append(RecipePreview(id=r["id"], title=title, image=r.get("image")))
        return results
    cached = db.query(RecipeCache).order_by(func.random()).limit(number).all()
    return [RecipePreview(id=c.id, title=c.title_ru if lang=="ru" else c.title_en, image=c.image) for c in cached]

async def search_recipe_by_name(db: Session, query: str, lang: str = "ru"):
    q_en = await translate_text(query, target='en') if bool(re.search('[а-яА-Я]', query)) else query
    data = await _make_request(f"{BASE_URL}/complexSearch", {"query": q_en, "number": 10})
    if data:
        results = []
        for r in data.get("results", []):
            title = await translate_text(r["title"]) if lang == "ru" else r["title"]
            results.append(RecipePreview(id=r["id"], title=title, image=r.get("image")))
        return results
    col = RecipeCache.title_ru if lang == "ru" else RecipeCache.title_en
    cached = db.query(RecipeCache).filter(col.ilike(f"%{query}%")).limit(10).all()
    return [RecipePreview(id=c.id, title=c.title_ru if lang=="ru" else c.title_en, image=c.image) for c in cached]

async def search_by_ingredients(db: Session, ingredients: str, lang: str = "ru"):
    ingr_en = await translate_text(ingredients, target='en') if bool(re.search('[а-яА-Я]', ingredients)) else ingredients
    data = await _make_request(f"{BASE_URL}/findByIngredients", {"ingredients": ingr_en, "number": 5})
    if data:
        results = []
        for r in data:
            title = await translate_text(r["title"]) if lang == "ru" else r["title"]
            results.append(RecipePreview(id=r["id"], title=title, image=r.get("image")))
        return results
    return list(db.query(RecipeCache).limit(5).all())

async def get_recipe_info(db: Session, recipe_id: int, lang: str = "ru"):
    data = await _make_request(f"{BASE_URL}/{recipe_id}/information", {"includeNutrition": "false"})
    if data:
        title = await translate_text(data["title"]) if lang == "ru" else data["title"]
        instr = await translate_text(data.get("instructions", "")) if lang == "ru" else data.get("instructions", "")
        ingr_raw = ", ".join([i.get("original", "") for i in data.get("extendedIngredients", [])])
        ingr = await translate_text(ingr_raw) if lang == "ru" else ingr_raw
        return RecipeFull(id=data["id"], title=title, image=data.get("image"), ingredients=ingr, instructions=instr)
    c = db.query(RecipeCache).filter(RecipeCache.id == recipe_id).first()
    if c:
        return RecipeFull(id=c.id, title=c.title_ru if lang=="ru" else c.title_en, 
                          image=c.image, ingredients=c.ingredients_ru if lang=="ru" else c.ingredients_en, 
                          instructions=c.instructions_ru if lang=="ru" else c.instructions_en)
    return None


async def get_substitute(ingredient: str):
    ingr_en = await translate_text(ingredient, target='en')
    url = f"https://api.spoonacular.com/recipes/food/ingredients/substitutes"
    data = await _make_request(url, {"ingredientName": ingr_en})
    if data and data.get("status") == "success":
        return await translate_text(data.get("substituteString"))
    return "К сожалению, не нашел замену этому продукту."