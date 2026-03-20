from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🎲 Рандомный рецепт", callback_data="random"))
    builder.add(InlineKeyboardButton(text="🔍 Поиск рецепта", callback_data="search_menu"))
    builder.add(InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile_menu"))
    builder.adjust(1)
    return builder.as_markup()


def search_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📝 По названию", callback_data="search_name"))
    builder.add(InlineKeyboardButton(text="🍅 По ингредиентам", callback_data="search_ingr"))
    builder.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="to_main"))
    builder.adjust(1)
    return builder.as_markup()

def profile_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⚖️ Изменить вес", callback_data="stub_action"))
    builder.add(InlineKeyboardButton(text="📏 Изменить рост", callback_data="stub_action"))
    builder.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="to_main"))
    builder.adjust(2, 1)
    return builder.as_markup()

def cancel_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Отменить и вернуться", callback_data="to_main"))
    return builder.as_markup()

def recipe_actions(recipe_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❤️ В избранное", callback_data=f"fav_{recipe_id}"))
    builder.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main_from_recipe"))
    builder.adjust(1)
    return builder.as_markup()