from decimal import Decimal

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage

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
