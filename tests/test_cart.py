import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from test_data.products import PRODUCTS

pytestmark = pytest.mark.regression


@pytest.mark.manual_script("MT-002")
@pytest.mark.p1
def test_remove_item_leaves_empty_cart(cart):
    cart.remove("Sauce Labs Backpack")
    expect(cart.items).to_have_count(0)
    cart.header.expect_count(0)


@pytest.mark.manual_script("MT-006")
@pytest.mark.p1
def test_cart_survives_navigation(cart, page):
    cart.continue_shopping()
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    inventory.expect_added("Sauce Labs Backpack")
    inventory.header.open_cart()
    cart.expect_loaded()
    cart.expect_item("Sauce Labs Backpack", "$29.99")
    cart.header.expect_count(1)


@pytest.mark.manual_script("MT-006")
@pytest.mark.p1
def test_cart_survives_refresh(cart):
    cart.refresh()
    cart.expect_loaded()
    cart.expect_item("Sauce Labs Backpack", "$29.99")
    cart.header.expect_count(1)


@pytest.mark.coverage_gap("G02")
@pytest.mark.p1
@pytest.mark.manual_script("MT-007")
def test_six_items_partial_removal_and_empty_cart(inventory, page):
    for product in PRODUCTS:
        inventory.add(product["name"])
    inventory.header.expect_count(6)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(6)
    for product in PRODUCTS:
        cart.expect_item(product["name"], product["price"])
    removed = "Sauce Labs Onesie"
    cart.remove(removed)
    cart.header.expect_count(5)
    expect(cart.item(removed)).to_have_count(0)
    remaining = [product for product in PRODUCTS if product["name"] != removed]
    expect(cart.items).to_have_count(5)
    for product in remaining:
        cart.expect_item(product["name"], product["price"])
    for index, product in enumerate(remaining, start=1):
        cart.remove(product["name"])
        expect(cart.item(product["name"])).to_have_count(0)
        expect(cart.items).to_have_count(len(remaining) - index)
        cart.header.expect_count(len(remaining) - index)
    cart.continue_shopping()
    inventory.expect_loaded()
    for product in PRODUCTS:
        inventory.expect_available(product["name"])


@pytest.mark.coverage_gap("G06")
@pytest.mark.p2
@pytest.mark.coverage_gap("G08")
@pytest.mark.manual_script("MT-008")
def test_cart_description_and_labels(cart):
    cart.expect_description(PRODUCTS[0]["name"], PRODUCTS[0]["description"])
    cart.expect_labels()
    cart.expect_common_layout()


@pytest.mark.coverage_gap("G04")
@pytest.mark.p1
@pytest.mark.observed_baseline
@pytest.mark.manual_script("MT-005")
def test_empty_cart_reaches_zero_total_overview(inventory, page, capture_page):
    """Observed 2026-09-25; does not declare that empty checkout should be allowed."""
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(0)
    cart.header.expect_count(0)
    cart.checkout()
    information = CheckoutInformationPage(page)
    information.expect_loaded()
    information.fill("QA", "Tester", "90210")
    information.continue_checkout()
    overview = CheckoutOverviewPage(page)
    overview.expect_loaded()
    expect(overview.items).to_have_count(0)
    expect(overview.subtotal).to_have_text("Item total: $0")
    expect(overview.tax).to_have_text("Tax: $0.00")
    expect(overview.total).to_have_text("Total: $0.00")
    overview.header.expect_count(0)
    capture_page("empty-cart-overview-observed-baseline")
    overview.cancel()
    inventory.expect_loaded()
    inventory.header.expect_count(0)
