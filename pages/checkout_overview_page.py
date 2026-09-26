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
        self.quantity_label = page.get_by_test_id("cart-quantity-label")
        self.description_label = page.get_by_test_id("cart-desc-label")
        self.payment_label = page.get_by_test_id("payment-info-label")
        self.payment_value = page.get_by_test_id("payment-info-value")
        self.shipping_label = page.get_by_test_id("shipping-info-label")
        self.shipping_value = page.get_by_test_id("shipping-info-value")
        self.total_label = page.get_by_test_id("total-info-label")

    def expect_loaded(self):
        self.expect_path("checkout-step-two.html")
        expect(self.page.get_by_test_id("title")).to_have_text("Checkout: Overview")
        expect(self.finish_button).to_be_visible()

    def expect_item_details(self, product: dict, quantity: int = 1):
        row = self.items.filter(has=self.page.get_by_text(product["name"], exact=True))
        expect(row).to_have_count(1)
        expect(row.get_by_test_id("inventory-item-desc")).to_have_text(product["description"])
        expect(row.get_by_test_id("inventory-item-price")).to_have_text(product["price"])
        expect(row.get_by_test_id("item-quantity")).to_have_text(str(quantity))

    def expect_summary_information(self):
        expect(self.quantity_label).to_have_text("QTY")
        expect(self.description_label).to_have_text("Description")
        expect(self.payment_label).to_have_text("Payment Information:")
        expect(self.payment_value).to_have_text("SauceCard #31337")
        expect(self.shipping_label).to_have_text("Shipping Information:")
        expect(self.shipping_value).to_have_text("Free Pony Express Delivery!")
        expect(self.total_label).to_have_text("Price Total")

    def finish(self):
        self.finish_button.click()

    def cancel(self):
        self.cancel_button.click()
