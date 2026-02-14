from models.base_models import MoviesResponse, Movie
from utils.data_generator import DataGenerator
import allure
import pytest


@allure.epic("Тестирование Movies API")
@allure.feature('Тестирование создания, обновления и удаления фильмов')
class TestMoviesAPI:

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.description("""
      Этот тест проверяет корректность получения всех фильмов.
      """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест на получения всех фильмов по get запросу')
    def test_get_movies(self, api_manager):
        """
        Получение фильмов с параметрами по умолчанию.
        """
        with allure.step('Отправка get-запроса на /movies ресурс'):
            response = api_manager.movies_api.get_movies()

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = MoviesResponse(**response.json()).model_dump()

        with allure.step("Проверяем что все фильмы пришли в json ответе"):
            assert "movies" in movies_response


    @pytest.mark.regression
    @allure.description("""
          Этот тест проверяет корректность создания фильмов.
          Шаги:
          1.Генерация рандомных данных фильма.
          2.Создание: Отправка рандомного фильма методом 'post' на ендпоинт "/movies"
          3.Проверка id созданого фильма в json ответе 
          4.Проверка названии фильма в json ответе 
          5.Проверка диапазона цены в json ответе 
          """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест создания рандомного фильма по "post" запросу')
    def test_create_movie(self, api_manager):
        """
        Тест на создание нового фильма.
        """
        with allure.step('Генерация случайных данных фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Создание:Отправка данных фильма через post-запрос на /movies endoint'):
            response = api_manager.movies_api.create_movie(data=movie_data)

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**response.json()).model_dump()

        with allure.step("Проверяем наличие ID фильма в json ответе"):
            assert "id" in movies_response

        with allure.step("Проверяем что название созданного фильма соответствует названию фильма в ответе json"):
            assert movies_response["name"] == movie_data["name"]

        with allure.step('Проверяем что цена созданного фильма соответствует цене фильма в json ответе'):
            assert movies_response["price"] == movie_data["price"]


    @pytest.mark.api
    @pytest.mark.regression
    @allure.description("""
              Этот тест проверяет корректность обновления фильмов.
              Шаги:
              1.Генерация рандомных данных фильма.
              2.Генерация данных для обновления фильма
              3.Создание: Отправка рандомного фильма методом 'post' на ендпоинт "/movies"
              4.Обновление: Отправка данных для обновления фильма методом 'PATCH' на ендпоинт "/movies"
              5.Проверка обновления названия фильма 
              5.Проверка обновления цены фильма 
              """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест обновления существующего фильма по "PATCH" методу')
    def test_update_movie(self, api_manager):
        """
        Обновление существующего фильма.
        """
        with allure.step('Генерация случайных данных фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Генерация случайных данных для обновления фильма'):
            updated_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Создание:Отправка данных фильма через post-запрос на /movies endoint'):
            response = api_manager.movies_api.create_movie(data=movie_data)

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**response.json()).model_dump()

        with allure.step('Отправка данных для обновления фильма через "PATCH" метод на /movies/id endoint'):
            response = api_manager.movies_api.update_movie(movie_id=movies_response['id'],data=updated_data)
            updated_movie = response.json()

        with allure.step("Проверяем что название обновленного фильма отличается от ранее созданного фильма"):
            assert movies_response ["name"] != updated_movie['name']

        with allure.step("Проверяем что цена обновленного фильма отличается от цены ранее созданного фильма"):
            assert movies_response ["price"] != updated_movie["price"]


    @pytest.mark.slow
    @pytest.mark.regression
    @allure.description("""
                  Этот тест проверяет корректность получения фильма по ID.
                  Шаги:
                  1.Генерация рандомных данных фильма.
                  2.Создание: Отправка рандомного фильма методом 'post' на ендпоинт "/movies"
                  4.Обновление: Отправка данных для обновления фильма методом 'PATCH' на ендпоинт "/movies"
                  5.Проверка обновления названия фильма 
                  5.Проверка обновления цены фильма 
                  """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест получения существующего фильма по ID по "GET" методу')
    def test_get_movie_by_id(self, api_manager):
        """
        Создаем фильм и получаем его по ID.
        """
        with allure.step('Генерация случайных данных фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Создание:Отправка данных фильма через post-запрос на /movies endoint'):
            created = api_manager.movies_api.create_movie(data=movie_data).json()

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**created).model_dump()

        with allure.step('Отправка данных для получения фильма по ID через "GET" метод на /movies/id endoint'):
            response = api_manager.movies_api.get_movie_by_id(movies_response['id']).json()

        with allure.step("Проверяем соответствие ID созданого фильма в ID фильму пришедшем в json ответе"):
            assert response["id"] == created['id']


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.description("""
                      Этот тест проверяет корректность удаления фильма по ID.
                      Шаги:
                      1.Генерация рандомных данных фильма.
                      2.Создание: Отправка рандомного фильма методом 'post' на ендпоинт "/movies"
                      4.Удаление: Отправка ID фильма методом 'DELETE' на ендпоинт "/movies/ID"
                      5.Проверка обновления названия фильма 
                      5.Проверка обновления цены фильма 
                      """)
    @allure.severity(allure.severity_level.NORMAL )
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест удаления существующего фильма по ID по "DELETE" методу')
    def test_delete_movie(self, api_manager):
        """
        Удаление фильма.
        """
        with allure.step('Генерация случайных данных фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Создание: Отправка данных фильма через post-запрос на /movies endoint'):
            created = api_manager.movies_api.create_movie(data=movie_data).json()

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**created).model_dump()

        with allure.step('Удаление: Отправка ID фильма через "DELETE" method на /movies/ID endoint'):
            api_manager.movies_api.delete_movie(movies_response['id'])

        with allure.step('Проверяем что повторное обращение к фильму возвращает - 404 error - Not found.'):
            response = api_manager.movies_api.get_movie_by_id(movies_response['id'], expected_status=404)
            assert response.status_code == 404


    @pytest.mark.skip(reason="Тест дубликат, через API")
    def test_delete_movie_by_id(self, api_manager):
        """
        Удаление фильма.
        """
        movie_data = DataGenerator.generate_random_movie_data_for_api()
        created = api_manager.movies_api.create_movie(data=movie_data).json()
        movie_id = created["id"]

        # Удаляем фильм
        api_manager.movies_api.delete_movie(movie_id)

        # Повторная попытка получения фильма должна вернуть 404
        response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert response.status_code == 404


    @pytest.mark.db
    @allure.description("""
                          Этот тест проверяет корректность удаления фильма по ID в DB.
                          Шаги:
                          1.Генерация рандомного фильма через фикстуру "created_test_movie".
                          2.Проверка что фильм создан по ID используя DBMovieHelper
                          4.Удаление фильма
                          5.Проверка что фильм не существует в DB. 
                          """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест удаления существующего фильма в DB по ID через sqlalchemy.orm/Session')
    def test_delete_db_movie_by_id(self, db_movie_helper, created_test_movie):
        with allure.step('Проверяем по ID что фильм существует в DB'):
            assert db_movie_helper.movie_exists_by_id(created_test_movie.id)

        with allure.step('Удаляем созданный фикстурой фильм в DB'):
            db_movie_helper.delete_movie(created_test_movie)

        with allure.step('Проверяем что созданный фикстурой фильм не существует в DB'):
            assert not db_movie_helper.movie_exists_by_id(created_test_movie.id)


    @pytest.mark.regression
    @allure.description("""
                      Этот тест проверяет корректность получения фильма по фильтрации по жанру и локации.
                      Шаги:
                      1.Отправка запроса фильма с фильтрами через фикстуру - pre_filtered_movie.
                      2.Проверка ответа на соответствие корректного возврата фильма, фильтрам. 
                      """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест получения существующего фильма по фильтрам по "GET" методу')
    def test_get_movies_with_location_filters(self, api_manager, pre_filtered_movie):
        """
        Проверка фильтрации по жанру и локации.
        """
        with allure.step('Отправляем запрос по ID используя фильм с фильтрами'):
            response = api_manager.movies_api.get_movie_by_id(pre_filtered_movie['id'])

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**response.json()).model_dump()

        with allure.step('Проверяем что "location" фильма ответа соответствует "location" отфильтрованному фильму'):
            assert movies_response["location"] == pre_filtered_movie["location"]

        with allure.step('Проверяем что "genreID" фильма ответа соответствует "genreID" отфильтрованному фильму'):
            assert movies_response["genreId"] == pre_filtered_movie["genreId"]

        with allure.step('Проверяем что "name" фильма ответа соответствует "name" отфильтрованному фильму'):
            assert movies_response["name"] == pre_filtered_movie["name"]


    @pytest.mark.negative
    @allure.description("""
                          Этот негативный тест проверяет корректность получения ответа по некорректной локации.
                          Шаги:
                          1.Отправка запроса фильма с фильтрами через фикстуру - pre_filtered_movie.
                          2.Проверка ответа на соответствие корректного возврата фильма, фильтрам. 
                          """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест обработки запроса на фильм с невалидной локацией')
    def test_get_movies_invalid_location(self, api_manager):
        """
        Негативный тест: передаем недопустимую локацию.
        """
        params = {
            "locations": "LA"  # допустимы только MSK, SPB
        }
        with allure.step('Отправляем запрос используя параметры с недопустимой локацией.'):
            response = api_manager.movies_api.get_movies(params=params, expected_status=400)
            data = response.json()

        with allure.step('Проверяем что в тексте ошибки есть - "Bad Request".'):
            assert data["error"] == "Bad Request"

        with allure.step('Проверяем что статус код равен - 400!.'):
            assert data["statusCode"] == 400

        with allure.step('Проверяем что сообщение ошибки содержит = "Некорректные данные"!'):
            assert data['message'] == 'Некорректные данные'


    @pytest.mark.slow
    @pytest.mark.regression
    @allure.description("""
                          Этот тест проверяет корректность создания фильма с ролью - SuperAdmin.
                          Шаги:
                           1.Генерация рандомных данных фильма.
                           2.Создание: Отправка SuperAdmin-ом рандомного фильма методом 'POST' на ендпоинт "/movies" 
                           3.Проверяем успешность статус кода - (201)
                           4.Проверяем что название созданного фильма соответствует сгенерированому фильму
                          """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест создание фильма SuperAdmin-ом')
    def test_create_movie_by_super_admin(self, super_admin):
        with allure.step('Генерация рандомного фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Отправка запроса на создание фильма с ролью - SuperAdmin'):
            response = super_admin.api.movies_api.create_movie(data=movie_data)

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**response.json()).model_dump()

        with allure.step('Проверка что название фильма ответа соответствует названию сгенерированного фильма'):
            assert movies_response["name"] == movie_data["name"]

        with allure.step('Проверка что цена фильма ответа соответствует цене сгенерированного фильма'):
            assert movies_response["price"] == movie_data["price"]


    @pytest.mark.api
    @pytest.mark.regression
    @allure.description("""
                  Этот тест проверяет корректность обновления фильмов с ролью - SuperAdmin.
                  Шаги:
                  1.Генерация рандомных данных фильма.
                  2.Генерация данных для обновления фильма
                  3.Создание: Отправка рандомного фильма методом 'POST' на ендпоинт "/movies"
                  4.Обновление: Отправка данных для обновления фильма методом 'PATCH' на ендпоинт "/movies"
                  5.Проверка обновления названия фильма после обновления
                  5.Проверка обновления цены фильма после обновления 
                  """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест обновления существующего фильма по "PATCH" методу')
    def test_update_movie_admin(self, super_admin):
        with allure.step('Генерация рандомного фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Генерация обновленных данных для фильма'):
            updated_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Отправка запроса на создание фильма с ролью - SuperAdmin'):
            created = super_admin.api.movies_api.create_movie(data=movie_data)

        with allure.step("Проверяем, что ответ соответствует ожидаемой структуре"):
            movies_response = Movie(**created.json()).model_dump()

        with allure.step('Отправка запроса на обновления фильма с ролью - SuperAdmin'):
            updated = super_admin.api.movies_api.update_movie(
            movie_id=movies_response["id"],
            data=updated_data
            ).json()

        with allure.step('Проверка что название созданного фильма отличается после отправки обновленных данных'):
            assert movies_response["name"] != updated["name"]

        with allure.step('Проверка что цена созданного фильма отличается после отправки обновленных данных'):
            assert movies_response["price"] != updated["price"]


    @pytest.mark.negative
    @allure.description("""
                             Этот негативный тест проверяет корректность обработки создания фильмов с ролью - USER.
                              Шаги:
                              1.Генерация рандомного фильма.
                              2.Отправка запроса на создание фильма с ролью - USER
                              3.Проверка что статус код = 403' 
                              4.Проверка в сообщение об ошибке содержится  = "Forbidden resource".
                       """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Негативный тест проверяет корректность обработки создания фильмов с ролью - USER')
    def test_create_movie_with_common_user(self, common_user):
        with allure.step('Генерация рандомного фильма'):
            movie_data = DataGenerator.generate_random_movie_data_for_api()

        with allure.step('Отправка запроса на создание фильма с ролью - USER'):
            response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)
            movie_data = response.json()

        with allure.step('Проверка что статус код = 403'):
            assert response.status_code == 403, 'какая то неизвестная ошибка'

        with allure.step('Проверка в сообщение об ошибке содержится  = "Forbidden resource".'):
            assert movie_data["message"] == "Forbidden resource"

    @pytest.mark.slow
    @allure.description("""
                          Этот тест проверяет корректность получения фильма используя параметризацию по фильтрам.
                          Шаги:
                          1.Отправка запроса фильма с фильтрами.
                          2.Проверка ответа на соответствие корректного возврата фильма, фильтрам. 
                          """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("AQA", "Dilovar")
    @allure.title('Тест получения существующего фильма используя параметризацию по фильтрам')
    @pytest.mark.parametrize(
        "price_from, price_to, locations, genre_id",
        [
            (0, 1000, "MSK", None),
            (None, None, ["MSK", "SPB"], None),
            (None, None, None, 1),
        ],
        ids=["Price range", "Locations", "Genre ID"]
    )
    def test_get_movies_with_filters(self,
            api_manager,
            price_from,
            price_to,
            locations,
            genre_id
    ):
        with allure.step("Собираем параметры фильтра"):
            params = DataGenerator.generate_movies_params(
                price_from=price_from,
                price_to=price_to,
                locations=locations,
                genre_id=genre_id
            )

        with allure.step(f"Отправляем запрос GET /movies с params={params}"):
            response = api_manager.movies_api.get_movies(params=params)

        with allure.step("Проверяем, что ответ соответствует схеме"):
            movies_response = MoviesResponse(**response.json())

        with allure.step("Проверяем, что фильмы соответствуют фильтрам"):
            for movie in movies_response.movies:

                if locations:
                    assert movie.location in locations, \
                        f"Локация {movie.location} не входит в {locations}"

                if genre_id is not None:
                    assert movie.genreId == genre_id

                if price_from is not None:
                    assert movie.price >= price_from

                if price_to is not None:
                    assert movie.price <= price_to




