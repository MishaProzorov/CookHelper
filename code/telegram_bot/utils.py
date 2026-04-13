# telegram_bot/utils.py
import re


async def format_recipe_card(recipe) -> str:
    title = recipe.title.upper() if recipe.title else "БЕЗ НАЗВАНИЯ"
    ingredients = recipe.ingredients if recipe.ingredients else "Не указаны"

    # Очищаем инструкции от HTML тегов
    instructions = re.sub('<[^<]+?>', '', recipe.instructions) if recipe.instructions else "Инструкция отсутствует."

    # Лимит Telegram для подписи к фото - 1024 символа.
    # Оставляем запас под заголовок и ссылку.
    if len(instructions) > 500:
        instructions = instructions[:500] + "..."

    text = (
        f"🍲 *{title}*\n\n"
        f"🛒 *Ингредиенты:*\n_{ingredients}_\n\n"
        f"👨‍🍳 *Инструкция:*\n{instructions}\n\n"
        f"🌐 [Открыть на сайте](http://127.0.0.1:8000/recipe/{recipe.id})"
    )
    return text