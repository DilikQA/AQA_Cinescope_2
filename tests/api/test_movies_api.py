from conftest import common_user
from utils.data_generator import DataGenerator
import pytest


class TestMoviesAPI:

    def test_get_movies(self, api_manager):
        """
        Получение фильмов с параметрами по умолчанию.
        """
        response = api_manager.movies_api.get_movies()
        data = response.json()
        assert "movies" in data


    def test_create_movie(self, api_manager):
        """
        Тест на создание нового фильма.
        """
        movie_data = DataGenerator.generate_random_movie_data()
        response = api_manager.movies_api.create_movie(data=movie_data)
        response_data = response.json()

        assert "id" in response_data
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]


    def test_update_movie(self, api_manager):
        """
        Обновление существующего фильма.
        """
        movie_data = DataGenerator.generate_random_movie_data()
        updated_data = DataGenerator.generate_random_movie_data()

        response = api_manager.movies_api.create_movie(data=movie_data)
        created_movie = response.json()
        response = api_manager.movies_api.update_movie(movie_id=created_movie['id'],data=updated_data)
        updated_movie = response.json()

        assert created_movie ["name"] != updated_movie['name']
        assert created_movie ["price"] != updated_movie["price"]

    def test_get_movie_by_id(self, api_manager):
        """
        Создаем фильм и получаем его по ID.
        """
        movie_data = DataGenerator.generate_random_movie_data()
        created = api_manager.movies_api.create_movie(data=movie_data).json()
        movie_id = created["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        response_data = response.json()

        assert response_data["id"] == movie_id



    def test_delete_movie(self, api_manager):
        """
        Удаление фильма.
        """
        movie_data = DataGenerator.generate_random_movie_data()
        created = api_manager.movies_api.create_movie(data=movie_data).json()
        movie_id = created["id"]

        # Удаляем фильм
        api_manager.movies_api.delete_movie(movie_id)

        # Повторная попытка получения фильма должна вернуть 404
        response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert response.status_code == 404

    def test_get_movies_with_filters(self, api_manager, pre_filtered_movie):
        """
        Проверка фильтрации по жанру и локации.
        """
        response = api_manager.movies_api.get_movie_by_id(pre_filtered_movie['id'])
        data = response.json()

        assert data["location"] == pre_filtered_movie["location"]
        assert data["genreId"] == pre_filtered_movie["genreId"]
        assert data["name"] == pre_filtered_movie["name"]

    def test_get_movies_invalid_location(self, api_manager):
        """
        Негативный тест: передаем недопустимую локацию.
        """
        params = {
            "locations": "LA"  # допустимы только MSK, SPB
        }

        response = api_manager.movies_api.get_movies(params=params, expected_status=400)
        data = response.json()

        assert data["error"] == "Bad Request"
        assert data["statusCode"] == 400
        assert data['message'] == 'Некорректные данные'

    def test_create_movie_by_super_admin(self, super_admin):
        movie_data = DataGenerator.generate_random_movie_data()

        response = super_admin.api.movies_api.create_movie(data=movie_data)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]

    def test_update_movie_admin(self, super_admin):
        movie_data = DataGenerator.generate_random_movie_data()
        updated_data = DataGenerator.generate_random_movie_data()

        created = super_admin.api.movies_api.create_movie(data=movie_data).json()
        updated = super_admin.api.movies_api.update_movie(
            movie_id=created["id"],
            data=updated_data
        ).json()

        assert created["name"] != updated["name"]
        assert created["price"] != updated["price"]

    def test_create_movie_with_common_user(self, common_user):
        movie_data = DataGenerator.generate_random_movie_data()
        response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)
        movie_data = response.json()

        assert response.status_code == 403, 'какая то неизвестная ошибка'
        assert movie_data["message"] == "Forbidden resource"



    @pytest.mark.parametrize(
        "price_from, price_to, locations, genre_id",
        [
            (0, 1000, "MSK", None),
            (None, None, ["MSK", "SPB"], None),
            (None, None, None, 1),
        ],
        ids=["Price range", "Locations", "Genre ID"]
    )
    def test_get_movies_with_filters(self, api_manager, price_from, price_to, locations, genre_id
    ):
        params = {}

        if price_from is not None:
            params["priceFrom"] = price_from
        if price_to is not None:
            params["priceTo"] = price_to
        if locations:
            params["locations"] = locations
        if genre_id:
            params["genreId"] = genre_id

        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        for movie in data["movies"]:
            if locations:
                assert movie["location"] in locations
            if genre_id:
                assert movie["genreId"] == genre_id
            if price_from:
                assert movie["price"] >= price_from



