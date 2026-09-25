import pytest

from pages.spinner_page import SpinnerPage


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_spinner_resolves_to_catalog(inventory, page, capture_page):
    inventory.header.open_dynamic_catalog("spinner")
    catalog = SpinnerPage(page)
    catalog.expect_loaded()
    catalog.expect_item(0, "Sauce Labs Bike Light", "$9.99")
    catalog.expect_item(5, "Sauce Labs Fleece Jacket", "$49.99")
    capture_page("spinner")
