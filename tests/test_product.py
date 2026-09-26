import pytest
from playwright.sync_api import expect

from pages.product_page import ProductPage

pytestmark = [pytest.mark.regression, pytest.mark.p2, pytest.mark.manual_script("MT-002")]


@pytest.mark.coverage_gap("G05")
def test_product_details_match_inventory(inventory, page, product):
    name = product["name"]
    price, description = inventory.product_details(name)
    inventory.open_product(name)
    details = ProductPage(page)
    details.expect_loaded(name)
    expect(details.price).to_have_text(price)
    expect(details.description).to_have_text(description)
    details.expect_common_layout()
    details.back()
    inventory.expect_loaded()


def test_add_remove_on_details_updates_inventory(inventory, page):
    name = "Sauce Labs Backpack"
    inventory.open_product(name)
    product = ProductPage(page)
    product.expect_loaded(name)
    product.add()
    product.header.expect_count(1)
    expect(product.remove_button).to_be_visible()
    product.remove()
    product.header.expect_count(0)
    expect(product.add_button).to_be_visible()
    product.back()
    inventory.expect_loaded()
    inventory.header.expect_count(0)
