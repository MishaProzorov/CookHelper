import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)


# 1. search_random_recipe() (не пустой)
@patch("services.recipe_service.search_random_recipe", new_callable=AsyncMock)
def test_search_random_recipe_not_empty(mock_service):
    # Подсовываем фейковый результат
    mock_service.return_value = [{"id": 1, "title": "Fake Pasta"}]

    response = client.get("/recipes/random")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Fake Pasta"


# 2. search_random_recipe() -параметр number
@patch("services.recipe_service.search_random_recipe", new_callable=AsyncMock)
def test_search_random_recipe_count(mock_service):
    # Имитируем возврат 5 рецептов
    mock_service.return_value = [{"id": i} for i in range(5)]

    response = client.get("/recipes/random?number=5")
    assert response.status_code == 200
    assert len(response.json()) == 5


# 3. search_recipe_by_name() - ответы чек
@patch("services.recipe_service.search_recipe_by_name", new_callable=AsyncMock)
def test_search_recipe_by_name_success(mock_service):
    mock_service.return_value = [{"id": 10, "title": "Pizza"}]

    response = client.get("/recipes/search?query=pizza")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "Pizza" in response.json()[0]["title"]


# 4. search_recipe_by_name() - Пустой ответ(ниче не нашли)
@patch("services.recipe_service.search_recipe_by_name", new_callable=AsyncMock)
def test_search_recipe_by_name_empty(mock_service):
    mock_service.return_value = []  # Ничего не нашли

    response = client.get("/recipes/search?query=unknown_dish")
    assert response.status_code == 200
    assert len(response.json()) == 0


# 5. search_by_ingredients() - Поиск по ингредиентам
@patch("services.recipe_service.search_by_ingredients", new_callable=AsyncMock)
def test_search_by_ingredients(mock_service):
    mock_service.return_value = [{"id": 123, "title": "Omelette"}]

    response = client.get("/recipes/by-ingredients?ingredients=egg,milk")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "Omelette"


# 6. get_recipe_info() - Получение информации по  ID
@patch("services.recipe_service.get_recipe_info", new_callable=AsyncMock)
def test_get_recipe_info_valid(mock_service):
    mock_service.return_value = {"id": 716429, "title": "Pasta With Garlic"}

    response = client.get("/recipes/716429/info")
    assert response.status_code == 200
    assert response.json()["id"] == 716429


# 7. get_recipe_info() - HTTPException 404 при несуществующем ID
@patch("services.recipe_service.get_recipe_info", new_callable=AsyncMock)
def test_get_recipe_info_invalid(mock_service):
    # Имитируем, что Spoonacular ничего не вернул
    mock_service.return_value = None

    response = client.get("/recipes/999999/info")
    assert response.status_code == 404
    assert response.json()["detail"] == "Рецепт не найден"