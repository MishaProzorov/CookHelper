import pytest
from fastapi.testclient import TestClient
from main import app
from database import session, Base, engine
import uuid
client = TestClient(app)


# Тест на странички(ручки)
@pytest.mark.parametrize("url", ["/", "/about", "/search", "/help"])
def test_pages_availability(url):
    response = client.get(url)
    assert response.status_code == 200


# Тест создания юзера
def test_create_user_db_logic():
    random_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    payload = {"gmail": random_email, "password": "password123"}
    response = client.post("/registration", data=payload, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "/"

# Тест удаления юзера
def test_delete_user_logic():
    user_id = 1
    response = client.delete(f"/registration/{user_id}")

    if response.status_code == 404:
        print("User not found, but endpoint exists")
    else:
        assert response.status_code == 200


# Чек БД на правильность всех полей и их наличие
def test_user_model_fields():
    from models import User
    user = User()
    assert hasattr(user, 'id')
    assert hasattr(user, 'gmail')
    assert hasattr(user, 'hashed_password')