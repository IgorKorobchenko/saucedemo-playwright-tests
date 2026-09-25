from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class LazyLoadPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")

    def expect_loaded(self):
        self.expect_path("dynamic-catalog-lazy-load.html")
        expect(self.title).to_have_text("Dynamic Catalog - Lazy Load")
        expect(self.page.get_by_test_id("lazy-load-item-0-name")).to_have_text("Sauce Labs Bike Light")

    def reveal_item(self, index: int):
        self.page.get_by_test_id(f"lazy-load-item-{index}").scroll_into_view_if_needed()

    def expect_item(self, index: int, name: str, price: str):
        expect(self.page.get_by_test_id(f"lazy-load-item-{index}-name")).to_have_text(name)
        expect(self.page.get_by_test_id(f"lazy-load-item-{index}-price")).to_have_text(price)
