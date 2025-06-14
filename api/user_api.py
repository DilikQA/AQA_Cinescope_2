from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, BASE_URL
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
       Класс для работы с API пользователей.
       """
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self.session = session
        super().__init__(session, self.USER_BASE_URL)


    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def clean_up_user(self, user_id, token):
        try:
            self.delete_user(user_id, token)
        except Exception as e:
            print(f"Не удалось удалить пользователя {user_id}: {e}")