from playwright.sync_api import Page, expect

from pages.footer import Footer
from pages.header import Header


class BasePage:
    """Shared browser operations; feature-specific locators live in page objects."""

    def __init__(self, page: Page):
        self.page = page

    def refresh(self):
        self.page.reload()

    def expect_path(self, path: str):
        expect(self.page).to_have_url(f"/{path}")

    def expect_common_layout(self):
        Header(self.page).expect_branding()
        Footer(self.page).expect_content()
