from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class CheckoutOverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = self.items.get_by_test_id("inventory-item-name")
        self.prices = self.items.get_by_test_id("inventory-item-price")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        self.cancel_button = page.get_by_test_id("cancel")

    def expect_loaded(self):
        self.expect_path("checkout-step-two.html")
        expect(self.finish_button).to_be_visible()

    def finish(self):
        self.finish_button.click()

    def cancel(self):
        self.cancel_button.click()
