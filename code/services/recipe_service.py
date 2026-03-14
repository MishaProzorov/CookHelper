import httpx

BASE_URL = "https://api.spoonacular.com/recipes"
API_KEY = "2fcd9d268a1e41f6b204d90be0801105"

async def search_random_recipe(number: int = 3):
    params = {"apiKey": API_KEY, "number": number}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/random", params=params)
        data = response.json()
        return data.get("recipes", [])
#получает список полной инфы очень очень много
#(не использовать для главной страницы слишком много инфы и муторно отсеивать)


#поиск по имени
async def search_recipe_by_name(query: str):
    params = {"apiKey": API_KEY, "query": query}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/complexSearch", params=params)
        data = response.json()

        return data.get("results", [])
#вот что получает по итогу в ответе
#       id": 646930,
#     "title": "Homemade Broccoli Cheddar Soup",
#     "image": "https://img.spoonacular.com/recipes/646930-312x231.jpg",
#     "imageType": "jpg"



async def search_by_ingredients(ingredients: str):
    params = {"apiKey": API_KEY, "ingredients": ingredients, "number": 5}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/findByIngredients", params=params)
        return response.json()

#получение фулл инфы по id
#сырая версия возвращает много инфы
async def get_recipe_info(recipe_id: int):
    params = {"apiKey": API_KEY}

    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/{recipe_id}/information"
        response = await client.get(url, params=params)

        return response.json()