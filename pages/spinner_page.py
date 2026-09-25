from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class SpinnerPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")
        self.spinner = page.get_by_test_id("dynamic-catalog-spinner")
        self.grid = page.get_by_test_id("dynamic-catalog-spinner-grid")

    def expect_loaded(self):
        self.expect_path("dynamic-catalog-spinner.html")
        expect(self.title).to_have_text("Dynamic Catalog - Spinner")
        expect(self.grid).to_be_visible(timeout=20_000)
        expect(self.spinner).to_be_hidden()

    def expect_item(self, index: int, name: str, price: str):
        expect(self.page.get_by_test_id(f"spinner-item-{index}-name")).to_have_text(name)
        expect(self.page.get_by_test_id(f"spinner-item-{index}-price")).to_have_text(price)
