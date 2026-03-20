def format_recipe_card(recipe: dict) -> str:

    title = recipe.get("title", "Неизвестное блюдо")
    time = recipe.get("readyInMinutes", "?")
    servings = recipe.get("servings", "?")


    ingredients_list = recipe.get("extendedIngredients", [])
    ingr_names = [ing.get("name", "") for ing in ingredients_list[:5]]
    ingr_text = ", ".join(ingr_names).capitalize()
    if len(ingredients_list) > 5:
        ingr_text += " и еще..."
    if not ingr_text:
        ingr_text = "Нет данных"


    nutrition_data = recipe.get("nutrition", {}).get("nutrients", [])

    if nutrition_data:
        # Если БЖУ есть, собираем его
        calories, protein, fat, carbs = "?", "?", "?", "?"
        for n in nutrition_data:
            if n["name"] == "Calories":
                calories = f"{n['amount']} {n['unit']}"
            elif n["name"] == "Protein":
                protein = f"{n['amount']} {n['unit']}"
            elif n["name"] == "Fat":
                fat = f"{n['amount']} {n['unit']}"
            elif n["name"] == "Carbohydrates":
                carbs = f"{n['amount']} {n['unit']}"

        stats_text = (
            f"📊 *Пищевая ценность:*\n"
            f"🔥 Калории: {calories}\n"
            f"🥩 Белки: {protein} | 🧈 Жиры: {fat} | 🍞 Углеводы: {carbs}"
        )
    else:

        veg = "✅" if recipe.get("vegetarian") else "❌"
        vegan = "✅" if recipe.get("vegan") else "❌"
        gf = "✅" if recipe.get("glutenFree") else "❌"
        likes = recipe.get("aggregateLikes", "0")
        health = recipe.get("healthScore", "?")

        stats_text = (
            f"📊 *Характеристики блюда:*\n"
            f"🥦 Вегетарианское: {veg}\n"
            f"🌱 Веганское: {vegan}\n"
            f"🌾 Без глютена: {gf}\n"
            f"❤️ Понравилось людям: {likes} | 💚 Индекс здоровья: {health}"
        )

    text = (
        f"🍲 *{title}*\n\n"
        f"⏱ *Время:* {time} мин | 🍽 *Порций:* {servings}\n\n"
        f"🛒 *Ингредиенты:*\n_{ingr_text}_\n\n"
        f"{stats_text}\n\n"
        f"🌐[Полный рецепт и инструкция на сайте](http://127.0.0.1:8000/recipes/{recipe.get('id')}/info)"
    )
    return text