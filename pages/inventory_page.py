from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.header import Header


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.names = self.items.get_by_test_id("inventory-item-name")
        self.prices = self.items.get_by_test_id("inventory-item-price")
        self.sort_control = page.get_by_test_id("product-sort-container")

    def expect_loaded(self):
        self.expect_path("inventory.html")
        expect(self.title).to_have_text("Products")
        expect(self.items.first).to_be_visible()

    def item(self, name: str):
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def add(self, name: str):
        self.item(name).get_by_role("button", name="Add to cart", exact=True).click()

    def remove(self, name: str):
        self.item(name).get_by_role("button", name="Remove", exact=True).click()

    def open_product(self, name: str):
        self.item(name).get_by_test_id("inventory-item-name").click()

    def product_details(self, name: str):
        row = self.item(name)
        return (
            row.get_by_test_id("inventory-item-price").inner_text(),
            row.get_by_test_id("inventory-item-desc").inner_text(),
        )

    def sort_by(self, value: str):
        self.sort_control.select_option(value)

    def expect_added(self, name: str):
        expect(self.item(name).get_by_role("button", name="Remove", exact=True)).to_be_visible()
        expect(self.item(name).get_by_role("button", name="Add to cart", exact=True)).to_have_count(0)
