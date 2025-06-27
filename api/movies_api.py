from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    BASE_URL = "https://api.dev-cinescope.coconutqa.ru"

    def __init__(self, session):
        super().__init__(session, self.BASE_URL)


    def get_movies(self, params=None, expected_status=200):
        """
        Получение информации о фильмах.
        :params: Данные для запроса фильмов.
        :params expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method='GET',
            endpoint="/movies",
            params=params,
            expected_status=expected_status)


    def create_movie(self, data,expected_status=200):
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=data,
            expected_status=expected_status
        )

    def update_movie(self, movie_id, data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            data=data,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма.
        :param movie_id: ID фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )
