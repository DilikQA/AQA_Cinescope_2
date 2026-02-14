from playwright.sync_api import Page
from page_object_models.base_page_actions import BasePage


class AllMoviesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}movies"

        # locators
        self.any_movie = "a[href='/movies/']"
        self.location_filter = "button[role='combobox' and text()='Место']"
        self.genre = "button[role='combobox' and text()='Жанр']"
        self.sort_by = "p 'Сортировка' button[role='combobox']"
        self.any_movie_learn_more_button = "a[href='/movies' and text()='Подробнее]'"

        # pagination
        self.pagination_container = "nav[role='navigation']"
        self.next_page = "nav[role='navigation'] button[aria-label='Go to next page']"
        self.prev_page = "nav[role='navigation'] button[aria-label='Go to previous page']"
        self.active_page = "nav[role='navigation'] a aria-current='page'"


    # Локальные action методы
    def open(self):
        self.open_url(self.url)

    def select_any_movie(self):
        self.page.locator(self.any_movie_learn_more_button).click()

    def choose_genre(self, genre_name: str):
        self.page.locator(self.genre).click()
        self.page.get_by_role("option", name=genre_name).click()


    def select_a_location(self, location: str):
        self.page.locator(self.location_filter).click()
        self.page.get_by_role("option", name=location).click()


    def sort_by_recency_created(self, recency):
        self.page.locator(self.sort_by).click()
        self.page.get_by_role("option", name=recency).click()

    def go_to_next_page(self):
        self.page.locator(self.next_page)

    def go_to_prev_page(self):
        self.page.locator(self.prev_page)



    def assert_was_redirect_to_movie_page(self, movie_id: int):
        expected_url = f"{self.home_url}movies/{movie_id}"
        self.wait_redirect_for_url(expected_url)






