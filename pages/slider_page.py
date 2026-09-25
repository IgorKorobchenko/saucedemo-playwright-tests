from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class SliderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")
        self.name = page.get_by_test_id("dynamic-catalog-slider-item-name")
        self.price = page.get_by_test_id("dynamic-catalog-slider-item-price")

    def expect_loaded(self):
        self.expect_path("dynamic-catalog-slider.html")
        expect(self.title).to_have_text("Dynamic Catalog - Slider")
        expect(self.name).to_be_visible()

    def select(self, index: int):
        self.page.get_by_test_id(f"dynamic-catalog-slider-dot-{index}").click()

    def expect_selection(self, index: int, name: str, price: str):
        expect(self.page.get_by_test_id(f"dynamic-catalog-slider-dot-{index}")).to_have_attribute("aria-current", "true")
        expect(self.name).to_have_text(name)
        expect(self.price).to_have_text(price)
