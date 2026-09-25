import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage


@pytest.mark.evidence
@pytest.mark.p3
@pytest.mark.manual_script("EXP-001")
@pytest.mark.manual_script("MT-008")
def test_capture_primary_pages(login, page, capture_page):
    """Automates the recorded tour, not open-ended discovery or visual judgment."""
    capture_page("login")
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    capture_page("inventory")
    inventory.open_product("Sauce Labs Backpack")
    product = ProductPage(page)
    product.expect_loaded("Sauce Labs Backpack")
    capture_page("product")
    product.add()
    product.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    capture_page("cart")
    cart.checkout()
    information = CheckoutInformationPage(page)
    information.expect_loaded()
    capture_page("checkout-information")
    information.fill("QA", "Tester", "90210")
    information.continue_checkout()
    overview = CheckoutOverviewPage(page)
    overview.expect_loaded()
    capture_page("checkout-overview")
    overview.finish()
    complete = CheckoutCompletePage(page)
    complete.expect_loaded()
    capture_page("checkout-complete")
    complete.back_home()
    inventory.expect_loaded()
    inventory.header.open_cart()
    cart.expect_loaded()
    expect(cart.items).to_have_count(0)


@pytest.mark.evidence
@pytest.mark.p3
@pytest.mark.manual_script("MT-008")
@pytest.mark.skip(reason="Approved design/copy or image baselines are not supplied. Captured screenshots require human review before visual pass/fail automation.")
def test_visual_approval_requires_baseline():
    """A screenshot capture alone cannot establish visual correctness."""
