import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage

pytestmark = [pytest.mark.regression, pytest.mark.p1]


@pytest.mark.manual_script("MT-002")
def test_remove_item_leaves_empty_cart(cart):
    cart.remove("Sauce Labs Backpack")
    expect(cart.items).to_have_count(0)
    cart.header.expect_count(0)


@pytest.mark.manual_script("MT-006")
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
def test_cart_survives_refresh(cart):
    cart.refresh()
    cart.expect_loaded()
    cart.expect_item("Sauce Labs Backpack", "$29.99")
    cart.header.expect_count(1)
