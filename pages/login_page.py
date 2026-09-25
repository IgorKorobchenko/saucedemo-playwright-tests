from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def open(self):
        self.page.goto("/")
        self.expect_loaded()

    def expect_loaded(self):
        expect(self.submit).to_be_visible()

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

    def expect_error(self, message: str):
        expect(self.error).to_have_text(message)
        expect(self.submit).to_be_visible()
