import asyncio, os, sys, logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

# Настройка путей
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)

from telegram_bot.keyboards import main_menu, authorized_profile_menu, cancel_menu, recipe_back
from telegram_bot.utils import format_recipe_card
from services.recipe_service import search_random_recipe, search_recipe_by_name, get_recipe_info
from services.user_service import get_user_by_gmail
from auth import verify_password
from database import session

load_dotenv(os.path.join(ROOT_DIR, ".env"))

ADMIN_ID = os.getenv("ADMIN_ID")
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


class BotState(StatesGroup):
    wait_name = State()
    wait_email = State()
    wait_password = State()
    wait_support = State()


# --- КОМАНДЫ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Мы НЕ очищаем state полностью, чтобы не стереть логин.
    # Очищаем только временные состояния ввода.
    current_data = await state.get_data()
    await state.set_state(None)
    await state.set_data(current_data)
    await message.answer("🍳 Привет! Я CookHelper. Что делаем?", reply_markup=main_menu())


@dp.callback_query(F.data == "to_main")
async def to_main(callback: types.CallbackQuery, state: FSMContext):
    # Возвращаемся в меню, сохраняя данные о логине
    current_data = await state.get_data()
    await state.set_state(None)
    await state.set_data(current_data)
    await callback.message.edit_text("🍳 Главное меню:", reply_markup=main_menu())


@dp.callback_query(F.data == "to_main_delete")
async def to_main_del(callback: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    await state.set_state(None)
    await state.set_data(current_data)
    await callback.message.delete()
    await callback.message.answer("🍳 Главное меню:", reply_markup=main_menu())


# --- ЛИЧНЫЙ КАБИНЕТ И АВТОРИЗАЦИЯ ---

@dp.callback_query(F.data == "profile_auth")
async def profile_hub(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    email = data.get("auth_email")

    if email:
        # ЕСЛИ ЗАЛОГИНЕН: Показываем кабинет
        text = f"👤 *ЛИЧНЫЙ КАБИНЕТ*\n\n✅ Статус: Авторизован\n📧 Почта: `{email}`\n\nЗдесь будут ваши настройки."
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=authorized_profile_menu())
    else:
        # ЕСЛИ НЕ ЗАЛОГИНЕН: Начинаем вход
        await state.set_state(BotState.wait_email)
        await callback.message.edit_text("📧 Вы не авторизованы.\nВведите вашу почту с сайта:",
                                         reply_markup=cancel_menu())


@dp.message(BotState.wait_email)
async def auth_email_input(message: types.Message, state: FSMContext):
    await state.update_data(temp_email=message.text)
    await state.set_state(BotState.wait_password)
    await message.answer("🔑 Введите пароль от аккаунта (сообщение удалится):")


@dp.message(BotState.wait_password)
async def auth_pass_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = data.get("temp_email")
    password = message.text

    try:
        await message.delete()  # Удаляем пароль для безопасности
    except:
        pass

    db = session()
    user = get_user_by_gmail(db, email)

    if user and verify_password(password, user.hashed_password):
        # СОХРАНЯЕМ ФАКТ ВХОДА В ПАМЯТЬ БОТА
        await state.update_data(auth_email=email)
        await state.set_state(None)
        await message.answer(f"🎉 Успешно! Теперь вы вошли как `{email}`", reply_markup=main_menu())
    else:
        await state.set_state(None)
        await message.answer("❌ Неверная почта или пароль.", reply_markup=main_menu())


@dp.callback_query(F.data == "logout_account")
async def logout_bot(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()  # Полностью очищаем память (стираем логин)
    await callback.answer("Вы вышли из аккаунта", show_alert=True)
    await callback.message.edit_text("🍳 Вы вышли. Главное меню:", reply_markup=main_menu())


# --- ТЕХПОДДЕРЖКА ---
@dp.callback_query(F.data == "support")
async def support_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState.wait_support)
    await callback.message.edit_text("🆘 Напишите ваш вопрос админу:", reply_markup=cancel_menu())


@dp.message(BotState.wait_support)
async def support_forward(message: types.Message, state: FSMContext):
    await state.set_state(None)
    if ADMIN_ID:
        user_info = f"{message.from_user.full_name} (ID: {message.from_user.id})"
        await bot.send_message(ADMIN_ID, f"📩 *ВОПРОС*\nОт: {user_info}\n\n{message.text}", parse_mode="Markdown")
        await message.answer("✅ Отправлено. Ждите ответа!", reply_markup=main_menu())


@dp.message(F.from_user.id == (int(ADMIN_ID) if ADMIN_ID else 0), F.reply_to_message)
async def support_answer(message: types.Message):
    try:
        user_id = int(message.reply_to_message.text.split("ID: ")[1].split("\n")[0])
        await bot.send_message(user_id, f"🔔 *ОТВЕТ ПОДДЕРЖКИ:*\n\n{message.text}", parse_mode="Markdown")
        await message.answer("✅ Доставлено.")
    except:
        await message.answer("❌ Ошибка ID.")


# --- ПОИСК И РАНДОМ (ОСТАЛОСЬ КАК БЫЛО) ---
@dp.callback_query(F.data == "random")
async def r_recipe(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    db = session()
    recipes = await search_random_recipe(db, number=1)
    if recipes:
        full = await get_recipe_info(db, recipes[0].id)
        text = await format_recipe_card(full)
        await callback.message.answer_photo(photo=full.image, caption=text, reply_markup=recipe_back(),
                                            parse_mode="Markdown")
    else:
        await callback.message.answer("Ошибка API", reply_markup=main_menu())


@dp.callback_query(F.data == "search_name")
async def s_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState.wait_name)
    await callback.message.edit_text("✍️ Что ищем?", reply_markup=cancel_menu())


@dp.message(BotState.wait_name)
async def s_name_res(message: types.Message, state: FSMContext):
    await state.set_state(None)
    db = session()
    res = await search_recipe_by_name(db, message.text)
    if res:
        full = await get_recipe_info(db, res[0].id)
        text = await format_recipe_card(full)
        await message.answer_photo(photo=full.image, caption=text, reply_markup=recipe_back(), parse_mode="Markdown")
    else:
        await message.answer("Ничего не найдено 😢", reply_markup=main_menu())


async def run():
    await bot.delete_webhook(drop_pending_updates=True)
    print("--- Бот запущен! ---")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())