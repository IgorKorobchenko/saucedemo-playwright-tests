from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.name = page.get_by_test_id("inventory-item-name")
        self.description = page.get_by_test_id("inventory-item-desc")
        self.price = page.get_by_test_id("inventory-item-price")
        self.add_button = page.get_by_test_id("add-to-cart")
        self.remove_button = page.get_by_test_id("remove")
        self.back_button = page.get_by_test_id("back-to-products")

    def expect_loaded(self, name: str):
        expect(self.back_button).to_be_visible()
        expect(self.name).to_have_text(name)

    def add(self):
        self.add_button.click()

    def remove(self):
        self.remove_button.click()

    def back(self):
        self.back_button.click()
