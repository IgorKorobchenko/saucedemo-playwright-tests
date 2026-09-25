from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = self.items.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_button = page.get_by_test_id("continue-shopping")

    def expect_loaded(self):
        self.expect_path("cart.html")
        expect(self.page.get_by_test_id("title")).to_have_text("Your Cart")

    def item(self, name: str):
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def expect_item(self, name: str, price: str, quantity: int = 1):
        row = self.item(name)
        expect(row).to_have_count(1)
        expect(row.get_by_test_id("inventory-item-price")).to_have_text(price)
        expect(row.get_by_test_id("item-quantity")).to_have_text(str(quantity))

    def remove(self, name: str):
        self.item(name).get_by_role("button", name="Remove", exact=True).click()

    def continue_shopping(self):
        self.continue_button.click()

    def checkout(self):
        self.checkout_button.click()
