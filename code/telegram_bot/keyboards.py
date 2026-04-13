from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🎲 Случайный рецепт", callback_data="random"))
    builder.add(InlineKeyboardButton(text="🔎 Поиск по названию", callback_data="search_name"))
    builder.add(InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile_auth")) # Переименовали
    builder.add(InlineKeyboardButton(text="🆘 Поддержка", callback_data="support"))
    builder.adjust(1)
    return builder.as_markup()

# Меню, которое видит залогиненный пользователь в кабинете
def authorized_profile_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🚪 Выйти из аккаунта", callback_data="logout_account"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="to_main"))
    builder.adjust(1)
    return builder.as_markup()

def cancel_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="to_main"))
    return builder.as_markup()

def recipe_back():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="to_main_delete"))
    return builder.as_markup()