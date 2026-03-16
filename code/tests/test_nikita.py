from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)


# 1. Тест на вход (Авторизация)
def test_login_success():
    # Генерируем почту через время, чтобы не повторялась (простой хак)
    email = f"user_{int(time.time())}@test.com"

    # Сначала регистрируем
    client.post("/registration", data={"gmail": email, "password": "123"})

    # Теперь логинимся
    response = client.post("/login", data={"gmail": email, "password": "123"}, follow_redirects=False)

    assert response.status_code == 302
    assert "my_token" in response.cookies


# 2. Тест на неправильный пароль (Безопасность)
def test_login_wrong_password():
    response = client.post("/login", data={"gmail": "admin@test.com", "password": "wrong"}, follow_redirects=False)
    assert response.status_code == 401


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