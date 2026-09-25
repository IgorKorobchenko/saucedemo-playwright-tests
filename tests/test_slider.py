import pytest

from pages.slider_page import SliderPage


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_select_product_slide(inventory, page, capture_page):
    inventory.header.open_dynamic_catalog("slider")
    catalog = SliderPage(page)
    catalog.expect_loaded()
    catalog.select(4)
    catalog.expect_selection(4, "Sauce Labs Backpack", "$29.99")
    capture_page("slider")
