from playwright.sync_api import Page, expect


class Header:
    """Shared header/menu component composed into authenticated pages."""

    def __init__(self, page: Page):
        self.page = page
        self.cart = page.get_by_test_id("shopping-cart-link")
        self.badge = page.get_by_test_id("shopping-cart-badge")
        self.open_menu = page.get_by_role("button", name="Open Menu", exact=True)
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.dynamic_catalog_link = page.get_by_test_id("dynamic-catalog-sidebar-link")

    def open_cart(self):
        self.cart.click()

    def logout(self):
        self.open_menu.click()
        self.logout_link.click()

    def open_dynamic_catalog(self, variant: str):
        self.open_menu.click()
        self.dynamic_catalog_link.click()
        self.page.get_by_test_id(f"dynamic-catalog-{variant}-link").click()

    def expect_count(self, count: int):
        if count:
            expect(self.badge).to_have_text(str(count))
        else:
            expect(self.badge).to_have_count(0)
