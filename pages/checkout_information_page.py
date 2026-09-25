from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class CheckoutInformationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.cancel_button = page.get_by_test_id("cancel")
        self.error = page.get_by_test_id("error")

    def expect_loaded(self):
        self.expect_path("checkout-step-one.html")
        expect(self.first_name).to_be_visible()

    def fill(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_checkout(self):
        self.continue_button.click()

    def cancel(self):
        self.cancel_button.click()

    def expect_error(self, message: str):
        expect(self.error).to_have_text(message)
        self.expect_loaded()
