"""Shared fixtures for isolated SauceDemo UI tests."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.products import PRODUCTS


def pytest_addoption(parser):
    parser.addoption("--update-visual-baselines", action="store_true", default=False,
                     help="Explicitly record current screenshots as visual regression baselines")


@pytest.fixture
def visual_check(page, browser, pytestconfig, output_path):
    from support.visual import assert_visual_baseline

    def check(name: str):
        assert_visual_baseline(
            page, browser, name,
            Path(pytestconfig.rootpath) / "tests" / "visual_baselines",
            Path(output_path),
            update=pytestconfig.getoption("--update-visual-baselines"),
        )

    return check


@pytest.fixture(params=PRODUCTS, ids=lambda product: product["name"])
def product(request):
    return request.param


@pytest.fixture(scope="session", autouse=True)
def configure_playwright(playwright):
    playwright.selectors.set_test_id_attribute("data-test")
    expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}}


@pytest.fixture
def login(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture
def inventory(login, page):
    # Public demo credentials displayed by the application; not private secrets.
    login.login("standard_user", "secret_sauce")
    inventory_page = InventoryPage(page)
    inventory_page.expect_loaded()
    inventory_page.header.expect_count(0)
    return inventory_page


@pytest.fixture
def cart(inventory, page):
    inventory.add("Sauce Labs Backpack")
    inventory.header.open_cart()
    cart_page = CartPage(page)
    cart_page.expect_loaded()
    cart_page.expect_item("Sauce Labs Backpack", "$29.99")
    return cart_page


@pytest.fixture
def checkout_information(cart, page):
    cart.checkout()
    information = CheckoutInformationPage(page)
    information.expect_loaded()
    return information


@pytest.fixture
def checkout_overview(checkout_information, page):
    checkout_information.fill("QA", "Tester", "90210")
    checkout_information.continue_checkout()
    overview = CheckoutOverviewPage(page)
    overview.expect_loaded()
    return overview


@pytest.fixture
def checkout_complete(checkout_overview, page):
    checkout_overview.finish()
    complete = CheckoutCompletePage(page)
    complete.expect_loaded()
    return complete


@pytest.fixture
def capture_page(page, browser, output_path):
    """Capture evidence for review; screenshots are never auto-approved baselines."""
    directory = Path(output_path)

    def capture(name: str):
        directory.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(directory / f"{name}.png"), full_page=True)
        data = {
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "url": page.url,
            "browser": browser.browser_type.name,
            "browser_version": browser.version,
            "viewport": page.viewport_size,
            "title": page.title(),
            "aria_snapshot": page.locator("body").aria_snapshot(),
            "review_status": "Not reviewed; not a visual pass/fail result",
        }
        (directory / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    return capture
