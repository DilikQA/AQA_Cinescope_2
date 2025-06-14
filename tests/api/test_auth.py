import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_login_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        # Авторизация
        login_response = api_manager.auth_api.login_user({
            "email": test_user["email"],
            "password": test_user["password"]
        })
        login_data = login_response.json()
        token = login_data["accessToken"]

        # Проверки
        assert "accessToken" in login_data
        assert login_data["user"]["email"] == test_user["email"]



