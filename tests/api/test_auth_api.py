from models.base_models import RegisterUserResponse
from api.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"



    def test_login_user(self, api_manager: ApiManager, test_user):
        """
        Тест на логирование пользователя.
        """
        # Авторизация
        response = api_manager.auth_api.register_user(user_data=test_user)
        login_response = api_manager.auth_api.login_user(
            {
            "email":  test_user.email,
            "password": test_user.password
            }
        )
        login_data = login_response.json()
        token = login_data["accessToken"]

        # Проверки
        assert "accessToken" in login_data
        assert login_data["user"]["email"] == test_user.email



