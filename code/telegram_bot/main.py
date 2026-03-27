import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from telegram_bot.keyboards import main_menu, search_menu, profile_menu, cancel_menu, recipe_actions
from telegram_bot.utils import format_recipe_card

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.recipe_service import search_random_recipe, search_recipe_by_name, search_by_ingredients, get_recipe_info

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


class SearchState(StatesGroup):
    waiting_for_name = State()
    waiting_for_ingredients = State()


# --- БАЗОВАЯ НАВИГАЦИЯ (Всегда можно нажать Назад) ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🍳 Добро пожаловать в CookHelper!", reply_markup=main_menu())


@dp.callback_query(F.data == "to_main")
async def to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()  # ВАЖНО: Если мы ждали текст, кнопка "Назад" сбросит ожидание!
    await callback.message.edit_text("🍳 Главное меню:", reply_markup=main_menu())


@dp.callback_query(F.data == "to_main_from_recipe")
async def to_main_from_recipe(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("🍳 Главное меню:", reply_markup=main_menu())


@dp.callback_query(F.data == "profile_menu")
async def open_profile(callback: types.CallbackQuery):
    text = "👤 *Твой профиль*\n\nПочта: _не привязана_\nРост: _не указан_\nВес: _не указан_"
    await callback.message.edit_text(text, reply_markup=profile_menu(), parse_mode="Markdown")


@dp.callback_query(F.data == "stub_action")
async def stub_action(callback: types.CallbackQuery):
    await callback.answer("Эта функция появится в следующем обновлении! 🛠", show_alert=True)


#рандом рецепты
@dp.callback_query(F.data == "random")
async def get_random(callback: types.CallbackQuery):
    await callback.message.delete()
    msg = await callback.message.answer("⏳ Готовлю случайное блюдо...")

    recipes = await search_random_recipe(number=1)
    if recipes:
        full_recipe = await get_recipe_info(recipes[0]['id'])
        await msg.delete()

        if full_recipe:
            text = format_recipe_card(full_recipe)
            keyboard = recipe_actions(full_recipe['id'])

            if full_recipe.get('image'):
                await callback.message.answer_photo(photo=full_recipe['image'], caption=text, reply_markup=keyboard,
                                                    parse_mode="Markdown")
            else:
                await callback.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await msg.delete()
        await callback.message.answer("Ошибка API :(", reply_markup=main_menu())


#поиск
@dp.callback_query(F.data == "search_menu")
async def show_search(callback: types.CallbackQuery):
    await callback.message.edit_text("🔍 Как будем искать?", reply_markup=search_menu())


@dp.callback_query(F.data == "search_name")
async def ask_recipe_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.waiting_for_name)
    # Выводим кнопку "Отмена", если юзер передумал писать
    await callback.message.edit_text("✍️ Напиши название блюда (на англ):", reply_markup=cancel_menu())


@dp.message(SearchState.waiting_for_name)
async def process_search_name(message: types.Message, state: FSMContext):
    await state.clear()
    msg = await message.answer("⏳ Ищу рецепты...")

    results = await search_recipe_by_name(message.text)
    await msg.delete()

    if results:
        full_recipe = await get_recipe_info(results[0]["id"])
        text = format_recipe_card(full_recipe)
        keyboard = recipe_actions(full_recipe['id'])
        await message.answer_photo(photo=full_recipe['image'], caption=text, reply_markup=keyboard,
                                   parse_mode="Markdown")
    else:
        await message.answer("Ничего не нашел по этому запросу 😢", reply_markup=main_menu())


@dp.callback_query(F.data == "search_ingr")
async def ask_ingredients(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.waiting_for_ingredients)
    await callback.message.edit_text("🍅 Напиши продукты через запятую (на англ):", reply_markup=cancel_menu())


@dp.message(SearchState.waiting_for_ingredients)
async def process_search_ingr(message: types.Message, state: FSMContext):
    await state.clear()
    msg = await message.answer("⏳ Изучаю твой холодильник...")

    results = await search_by_ingredients(message.text)
    await msg.delete()

    if results:
        full_recipe = await get_recipe_info(results[0]["id"])
        text = format_recipe_card(full_recipe)
        keyboard = recipe_actions(full_recipe['id'])
        await message.answer_photo(photo=full_recipe['image'], caption=text, reply_markup=keyboard,
                                   parse_mode="Markdown")
    else:
        await message.answer("Из этих продуктов ничего не приготовить 😢", reply_markup=main_menu())


@dp.callback_query(F.data.startswith("fav_"))
async def add_to_fav(callback: types.CallbackQuery):
    await callback.answer("Рецепт сохранен в избранное! ❤️", show_alert=True)


async def run_bot():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())