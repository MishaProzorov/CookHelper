import pytest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.user_service import current_user, get_user_by_gmail, delete_user
from models import User
from database import Base
from auth import security, get_password_hashe
from fastapi import Request, HTTPException
import asyncio

# Тестовая БД (SQLite в памяти)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Создаёт тестовую БД перед каждым тестом"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db):
    """Создаёт тестового пользователя"""
    user = User(
        gmail="testuser@example.com",
        hashed_password=get_password_hashe("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_mock_request(cookies: dict = None) -> Request:
    """Создаёт мок запроса с cookies"""
    mock_request = Mock(spec=Request)
    mock_request.cookies = cookies or {}
    return mock_request


class TestCurrentUser:
    """Тесты для функции current_user()"""

    def test_no_token_returns_none(self, db):
        """Тест 1: Без токена возвращает None"""
        request = create_mock_request(cookies={})
        
        result = asyncio.run(current_user(request, db))
        
        assert result is None

    def test_valid_token_returns_user(self, db, test_user):
        """Тест 2: С валидным токеном возвращает пользователя"""
        # Создаём валидный токен для пользователя
        token = security.create_access_token(uid=str(test_user.id))
        
        request = create_mock_request(cookies={"my_token": token})
        
        result = asyncio.run(current_user(request, db))
        
        assert result is not None
        assert result.id == test_user.id
        assert result.gmail == test_user.gmail

    def test_invalid_token_returns_none(self, db):
        """Тест 3: С невалидным токеном возвращает None"""
        invalid_token = "invalid_token_12345"
        
        request = create_mock_request(cookies={"my_token": invalid_token})
        
        result = asyncio.run(current_user(request, db))
        
        assert result is None

    def test_token_with_nonexistent_user_returns_none(self, db):
        """Тест 4: Токен с несуществующим user_id возвращает None"""
        # Создаём токен для несуществующего пользователя (id=99999)
        token = security.create_access_token(uid="99999")

        request = create_mock_request(cookies={"my_token": token})

        result = asyncio.run(current_user(request, db))

        assert result is None


class TestGetUserByGmail:
    """Тесты для функции get_user_by_gmail()"""

    def test_find_existing_user_by_gmail(self, db, test_user):
        """Тест 1: Находит существующего пользователя по gmail"""
        result = get_user_by_gmail(db, test_user.gmail)

        assert result is not None
        assert result.id == test_user.id
        assert result.gmail == test_user.gmail

    def test_nonexistent_gmail_returns_none(self, db):
        """Тест 2: Возвращает None если пользователь не найден"""
        result = get_user_by_gmail(db, "nonexistent@example.com")

        assert result is None


class TestDeleteUser:
    """Тесты для функции delete_user()"""

    def test_delete_existing_user(self, db, test_user):
        """Тест 1: Успешное удаление существующего пользователя"""
        result = delete_user(test_user.id, db)

        assert result is not None
        assert result.id == test_user.id
        # Проверяем что пользователь удалён из БД
        deleted = db.query(User).filter(User.id == test_user.id).first()
        assert deleted is None

    def test_delete_nonexistent_user_raises_404(self, db):
        """Тест 2: Вызывает HTTPException 404 при удалении несуществующего"""
        nonexistent_id = 99999

        with pytest.raises(HTTPException) as exc_info:
            delete_user(nonexistent_id, db)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Невозможно удалить пользователя."
