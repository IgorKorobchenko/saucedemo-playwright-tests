import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.manual_script("MT-001")
def test_complete_purchase_and_return_home(checkout_complete, page):
    checkout_complete.header.expect_count(0)
    checkout_complete.back_home()
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    inventory.header.expect_count(0)
    inventory.header.open_cart()
    cart = CartPage(page)
    cart.expect_loaded()
    expect(cart.items).to_have_count(0)


@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_download_order_pdf(checkout_complete, tmp_path):
    target = tmp_path / "order.pdf"
    filename = checkout_complete.download_pdf(target)
    assert filename.startswith("swag-labs-order-")
    assert filename.endswith(".pdf")
    assert target.read_bytes().startswith(b"%PDF-")
