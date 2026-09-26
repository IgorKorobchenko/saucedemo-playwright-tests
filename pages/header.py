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
        self.close_menu_button = page.get_by_role("button", name="Close Menu", exact=True)
        self.about_link = page.get_by_test_id("about-sidebar-link")
        self.logo = page.locator(".app_logo")

    def expect_branding(self):
        expect(self.logo).to_be_visible()
        expect(self.logo).to_have_text("Swag Labs")
        expect(self.cart).to_be_visible()
        expect(self.open_menu).to_be_visible()

    def expand_menu(self):
        self.open_menu.click()
        expect(self.about_link).to_be_visible()
        expect(self.close_menu_button).to_be_visible()

    def close_menu(self):
        self.close_menu_button.click()
        expect(self.about_link).to_be_hidden()
        expect(self.logout_link).to_be_hidden()
        expect(self.close_menu_button).to_be_hidden()

    def open_about(self):
        self.expand_menu()
        expect(self.about_link).to_have_attribute("href", "https://saucelabs.com/")
        self.about_link.click()

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
