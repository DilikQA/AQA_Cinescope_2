from constants import Roles
from models.base_models import UserResponse

class TestUser:
    def test_create_user(self, super_admin, creation_user_data):
        response_json = super_admin.api.user_api.create_user(creation_user_data).json()
        response_model = UserResponse(**response_json)

        assert response_model.id != ""
        assert response_model.email == creation_user_data.email
        assert response_model.fullName == creation_user_data.fullName
        assert response_model.roles == [role.value for role in creation_user_data.roles]
        assert response_model.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        # Создаём пользователя
        created_user_response_dict = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user_response = UserResponse(**created_user_response_dict)

        # Получаем пользователя по ID
        response_model_id = super_admin.api.user_api.get_user(created_user_response.id).json()
        response_model_id = UserResponse(**response_model_id)
        # Получаем пользователя по email
        response_model_email = super_admin.api.user_api.get_user(created_user_response.email).json()
        response_model_email = UserResponse(**response_model_email)

        # Проверки
        assert response_model_id is not None, "get_user() вернул None"
        assert response_model_id.id != '', "ID должен быть не пустым"
        assert response_model_id.email == creation_user_data.email
        assert response_model_id.fullName == creation_user_data.fullName
        assert response_model_id.roles == [role.value for role in creation_user_data.roles]
        assert response_model_id.verified is True


