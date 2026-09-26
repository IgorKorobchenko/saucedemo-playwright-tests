from decimal import Decimal

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.products import PRODUCTS

pytestmark = pytest.mark.regression


@pytest.mark.p0
@pytest.mark.manual_script("MT-001")
def test_overview_item_and_total(checkout_overview):
    expect(checkout_overview.names).to_have_text(["Sauce Labs Backpack"])
    expect(checkout_overview.prices).to_have_text(["$29.99"])
    expect(checkout_overview.subtotal).to_have_text("Item total: $29.99")
    # $2.40 is an observed baseline for this item, not an inferred universal tax rule.
    expect(checkout_overview.tax).to_have_text("Tax: $2.40")
    expect(checkout_overview.total).to_have_text("Total: $32.39")
    subtotal = Decimal(checkout_overview.subtotal.inner_text().split("$")[1])
    tax = Decimal(checkout_overview.tax.inner_text().split("$")[1])
    total = Decimal(checkout_overview.total.inner_text().split("$")[1])
    assert total == subtotal + tax


@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_cancel_returns_to_products_with_item(checkout_overview, page):
    checkout_overview.cancel()
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    inventory.expect_added("Sauce Labs Backpack")
    inventory.header.expect_count(1)


@pytest.mark.p2
@pytest.mark.coverage_gap("G06")
@pytest.mark.coverage_gap("G08")
@pytest.mark.manual_script("MT-008")
def test_overview_details_and_summary_sections(checkout_overview):
    checkout_overview.expect_item_details(PRODUCTS[0])
    checkout_overview.expect_summary_information()
    checkout_overview.expect_common_layout()
