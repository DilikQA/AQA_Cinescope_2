from page_object_models.base_page_actions import BasePage
from playwright.sync_api import Page


class MoviePage(BasePage):
    def __init__(self, page:Page, movie_title: str, movie_id: int):
        super().__init__(page)
        self.movie_title = movie_title
        self.movie_id = movie_id
        self.url = f"{self.home_url}movies/{self.movie_id}"

        #locatiors
        self.buy_button = 'a[href="/payment?movieId="]'
        self.input_testimonial_field = 'textarea[name="text"]'
        self.rating_filter = page.get_by_text("Оценка:").locator("..").get_by_role("combobox")
        self.send_button ='button[type="submit"]'

    def open(self):
        self.open_url(self.url)

    def click_on_buy_button(self):
        self.page.locator(self.buy_button).click()

    def select_rating(self, rating):
        self.rating_filter.click()
        self.page.get_by_role("option", name=rating).click()

    def input_testimonial(self, testimonial_text):
        self.enter_text_to_element(self.input_testimonial_field,testimonial_text)


    def click_on_send_button(self):
        self.page.locator(self.send_button).click()

    def assert_alert_was_pop_up(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")

