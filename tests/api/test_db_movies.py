from conftest import created_test_user


class TestDBRequests:

    def test_db_requests(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")


    def test_movie_crud(self, super_admin, db_movie_helper, movie_data):
        #Проверяем, что фильма ещё нет в базе
        assert db_movie_helper.get_movie_by_id(movie_data.id) is None, "Фильм уже существует в базе до теста"

        movie = db_movie_helper.create_test_movie(movie_data)
        movie_from_db = db_movie_helper.get_movie_by_id(movie_data["id"])
        # Проверяем, что фильм появился в базе
        assert movie.id == movie_from_db.id
        assert movie.name == movie_from_db.name
        assert movie.price == movie_from_db.price



