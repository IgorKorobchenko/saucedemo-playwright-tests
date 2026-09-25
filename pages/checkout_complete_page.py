from pathlib import Path

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class CheckoutCompletePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.message = page.get_by_test_id("complete-header")
        self.back_button = page.get_by_test_id("back-to-products")
        self.pdf_button = page.get_by_test_id("generate-pdf-order")

    def expect_loaded(self):
        self.expect_path("checkout-complete.html")
        expect(self.message).to_have_text("Thank you for your order!")

    def back_home(self):
        self.back_button.click()

    def download_pdf(self, target: Path):
        with self.page.expect_download() as event:
            self.pdf_button.click()
        download = event.value
        assert download.failure() is None
        download.save_as(target)
        return download.suggested_filename
