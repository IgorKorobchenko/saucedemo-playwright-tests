from decimal import Decimal

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from test_data.products import PRODUCTS

pytestmark = pytest.mark.regression


@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
@pytest.mark.parametrize("sort_order", ["az", "za", "lohi", "hilo"])
def test_sort_products(inventory, sort_order):
    names = inventory.names.all_text_contents()
    prices = inventory.prices.all_text_contents()
    inventory.sort_by(sort_order)
    if sort_order in ("az", "za"):
        expect(inventory.names).to_have_text(sorted(names, reverse=sort_order == "za"))
    else:
        expected = sorted(prices, key=lambda value: Decimal(value.lstrip("$")), reverse=sort_order == "hilo")
        expect(inventory.prices).to_have_text(expected)


@pytest.mark.p1
@pytest.mark.manual_script("MT-007")
def test_add_control_becomes_remove_and_can_be_used_again(inventory, page):
    name = "Sauce Labs Backpack"
    inventory.add(name)
    inventory.expect_added(name)
    inventory.header.expect_count(1)
    inventory.remove(name)
    inventory.header.expect_count(0)
    inventory.add(name)
    inventory.expect_added(name)
    inventory.header.expect_count(1)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(1)
    cart.expect_item(name, "$29.99", quantity=1)


@pytest.mark.p1
@pytest.mark.manual_script("MT-006")
def test_added_item_survives_inventory_refresh(inventory, page):
    inventory.add("Sauce Labs Backpack")
    inventory.refresh()
    inventory.expect_loaded()
    inventory.expect_added("Sauce Labs Backpack")
    inventory.header.expect_count(1)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    cart.expect_item("Sauce Labs Backpack", "$29.99")


@pytest.mark.p1
@pytest.mark.manual_script("MT-002")
def test_logout(inventory, page):
    inventory.header.logout()
    LoginPage(page).expect_loaded()


@pytest.mark.p1
@pytest.mark.coverage_gap("G01")
@pytest.mark.manual_script("MT-002")
def test_each_product_maps_to_correct_cart_row(inventory, page, product):
    inventory.add(product["name"])
    inventory.expect_added(product["name"])
    inventory.header.expect_count(1)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(1)
    cart.expect_item(product["name"], product["price"])
    cart.expect_description(product["name"], product["description"])


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.coverage_gap("G02")
@pytest.mark.manual_script("MT-002")
def test_two_product_cart(inventory, page):
    selected = PRODUCTS[:2]
    for count, product in enumerate(selected, start=1):
        inventory.add(product["name"])
        inventory.header.expect_count(count)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(2)
    for product in selected:
        cart.expect_item(product["name"], product["price"])


@pytest.mark.p1
@pytest.mark.coverage_gap("G02")
@pytest.mark.manual_script("MT-007")
def test_remove_all_products_from_inventory(inventory, page):
    for count, product in enumerate(PRODUCTS, start=1):
        inventory.add(product["name"])
        inventory.expect_added(product["name"])
        inventory.header.expect_count(count)
    for index, product in enumerate(PRODUCTS, start=1):
        inventory.remove(product["name"])
        inventory.expect_available(product["name"])
        inventory.header.expect_count(len(PRODUCTS) - index)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(0)


@pytest.mark.p2
@pytest.mark.coverage_gap("G05")
@pytest.mark.manual_script("MT-008")
def test_catalog_contains_all_expected_products(inventory):
    expect(inventory.items).to_have_count(len(PRODUCTS))
    expect(inventory.names).to_have_text([product["name"] for product in PRODUCTS])


@pytest.mark.p2
@pytest.mark.coverage_gap("G05")
@pytest.mark.manual_script("MT-008")
def test_product_card_content_and_loaded_image(inventory, product):
    inventory.expect_product_card(product)


@pytest.mark.p2
@pytest.mark.coverage_gap("G07")
@pytest.mark.manual_script("MT-002")
def test_menu_closes_and_underlying_page_is_usable(inventory):
    inventory.header.expand_menu()
    inventory.header.close_menu()
    inventory.add("Sauce Labs Backpack")
    inventory.header.expect_count(1)
    inventory.header.expand_menu()
    inventory.header.close_menu()


@pytest.mark.p2
@pytest.mark.coverage_gap("G07")
@pytest.mark.manual_script("MT-002")
def test_about_navigates_to_sauce_labs(inventory, page):
    # Test SauceDemo's outgoing navigation, not third-party availability/content.
    destination = "https://saucelabs.com/"
    page.route(destination, lambda route: route.fulfill(
        status=200, content_type="text/html", body="<title>External destination stub</title>"
    ))
    with page.expect_request(destination) as event:
        inventory.header.open_about()
    assert event.value.is_navigation_request()
    expect(page).to_have_url(destination)


@pytest.mark.p3
@pytest.mark.coverage_gap("G08")
@pytest.mark.manual_script("MT-008")
def test_inventory_branding_and_footer(inventory):
    inventory.expect_common_layout()
