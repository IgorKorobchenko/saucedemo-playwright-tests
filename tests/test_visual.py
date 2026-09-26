import pytest

from pages.product_page import ProductPage

pytestmark = [
    pytest.mark.regression,
    pytest.mark.visual,
    pytest.mark.observed_baseline,
    pytest.mark.p3,
    pytest.mark.manual_script("MT-008"),
    pytest.mark.browser_context_args(
        viewport={"width": 1280, "height": 800},
        device_scale_factor=1,
        color_scheme="light",
        reduced_motion="reduce",
        locale="en-US",
    ),
]


@pytest.fixture(scope="module")
def browser(browser_type):
    """Use the bundled headless browser even when functional tests use --headed."""
    browser = browser_type.launch(headless=True)
    yield browser
    browser.close()


@pytest.mark.parametrize("page_fixture", [
    "login", "inventory", "cart", "checkout_information", "checkout_overview", "checkout_complete",
])
def test_page_matches_visual_baseline(request, page_fixture, visual_check):
    request.getfixturevalue(page_fixture)
    visual_check(page_fixture)


def test_product_matches_visual_baseline(inventory, page, visual_check):
    inventory.open_product("Sauce Labs Backpack")
    product = ProductPage(page)
    product.expect_loaded("Sauce Labs Backpack")
    visual_check("product")
