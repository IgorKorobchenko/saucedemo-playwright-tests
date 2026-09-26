import pytest

from pages.cart_page import CartPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.p1
@pytest.mark.manual_script("MT-003")
@pytest.mark.parametrize("first,last,postal,message", [
    ("", "Tester", "90210", "Error: First Name is required"),
    ("QA", "", "90210", "Error: Last Name is required"),
    ("QA", "Tester", "", "Error: Postal Code is required"),
    ("", "", "", "Error: First Name is required"),
])
def test_required_fields_and_recovery(checkout_information, page, first, last, postal, message):
    checkout_information.fill(first, last, postal)
    checkout_information.continue_checkout()
    checkout_information.expect_error(message)
    checkout_information.fill("QA", "Tester", "90210")
    checkout_information.continue_checkout()
    CheckoutOverviewPage(page).expect_loaded()


@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_cancel_returns_to_cart(checkout_information, page):
    checkout_information.cancel()
    cart = CartPage(page)
    cart.expect_loaded()
    cart.expect_item("Sauce Labs Backpack", "$29.99")


@pytest.mark.p2
@pytest.mark.manual_script("MT-005")
@pytest.mark.observed_baseline
@pytest.mark.parametrize("first,last,postal", [
    pytest.param("A", "B", "1", id="single-character"),
    pytest.param(" ", " ", " ", id="whitespace-only"),
    pytest.param(" QA ", " Tester ", " 90210 ", id="surrounding-whitespace"),
    pytest.param("Élodie", "李", "Å1", id="unicode"),
    pytest.param("A" * 256, "B" * 256, "1" * 256, id="256-characters"),
])
def test_checkout_sampled_inputs_follow_observed_behavior(checkout_information, page, first, last, postal):
    """Current behavior, not an approved format/length policy; 256 is a sample, not a limit."""
    checkout_information.fill(first, last, postal)
    checkout_information.expect_values(first, last, postal)
    checkout_information.continue_checkout()
    overview = CheckoutOverviewPage(page)
    overview.expect_loaded()
    overview.header.expect_count(1)
    overview.cancel()
    InventoryPage(page).expect_loaded()


@pytest.mark.p3
@pytest.mark.coverage_gap("G08")
@pytest.mark.manual_script("MT-008")
def test_information_page_branding_and_footer(checkout_information):
    checkout_information.expect_common_layout()
