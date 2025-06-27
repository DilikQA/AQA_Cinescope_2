from utils.data_generator import DataGenerator

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
        assert data['message'] == ['Каждое значение в поле locations должно быть одним из значений: MSK, SPB']




