import pytest
import allure
from page_object_models.movie_page_object import MoviePage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Оставления отзывов под фильмом")
@pytest.mark.ui
class TestMovieTestimonials:
    @allure.title("Тест на успешное оставление отзыва")
    def test_put_testimonials_by_ui(self, logged_in_user_page):

        movie_page = MoviePage(logged_in_user_page, movie_title="Kristine Jackson", movie_id=13378)
        movie_page.open()
        movie_page.input_testimonial("Фильм топ 🔥")
        movie_page.click_on_send_button()

        movie_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
        movie_page.assert_alert_was_pop_up()  # Проверка появления и исчезновения алерта


