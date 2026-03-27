import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram_bot.main import cmd_start, get_random


@pytest.mark.asyncio
async def test_cmd_start_logic():

    mock_message = AsyncMock(spec=Message)
    mock_state = AsyncMock(spec=FSMContext)

    mock_message.answer = AsyncMock()

    await cmd_start(mock_message, mock_state)

    # Проверки
    mock_state.clear.assert_called_once()
    mock_message.answer.assert_called_once()

    args, kwargs = mock_message.answer.call_args
    assert "CookHelper" in args[0]


@pytest.mark.asyncio
@patch("telegram_bot.main.search_random_recipe", new_callable=AsyncMock)
@patch("telegram_bot.main.get_recipe_info", new_callable=AsyncMock)
async def test_get_random_recipe_bot(mock_get_info, mock_search_random):

    mock_search_random.return_value = [{"id": 123}]
    mock_get_info.return_value = {
        "id": 123,
        "title": "Тестовая Пицца",
        "image": "http://fake-image.url/pizza.jpg",
        "readyInMinutes": 30,
        "servings": 2
    }

    mock_callback = AsyncMock(spec=CallbackQuery)
    mock_callback.message = AsyncMock(spec=Message)

    mock_callback.answer = AsyncMock()
    mock_callback.message.delete = AsyncMock()
    mock_callback.message.answer_photo = AsyncMock()
    mock_callback.message.answer = AsyncMock()

    await get_random(mock_callback)

    # 4. Проверки
    mock_callback.message.delete.assert_called()

    mock_callback.message.answer_photo.assert_called_once()

    _, kwargs = mock_callback.message.answer_photo.call_args
    assert "Тестовая Пицца" in kwargs["caption"]