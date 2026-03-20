from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)



# 3. Тест на получение рандомных рецептов (Твой API сервис)
def test_get_random():
    response = client.get("/recipes/random")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # проверяем что пришел список


# 4. Тест на поиск рецептов
def test_search_recipe():
    response = client.get("/recipes/search?query=pasta")
    assert response.status_code == 200
    assert len(response.json()) >= 0