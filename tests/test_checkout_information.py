import pytest

from pages.cart_page import CartPage
from pages.checkout_overview_page import CheckoutOverviewPage

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
@pytest.mark.skip(reason="No approved checkout length/format/whitespace rules. Whitespace-only values were accepted during exploration; clarify intended behavior before pass/fail gating.")
def test_checkout_input_boundaries_require_confirmed_rules():
    """Explicit coverage gap; do not invent a maximum length or a rejection rule."""
