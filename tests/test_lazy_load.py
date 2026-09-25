import pytest

from pages.lazy_load_page import LazyLoadPage


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.manual_script("MT-002")
def test_scroll_reveals_later_item(inventory, page, capture_page):
    inventory.header.open_dynamic_catalog("lazy-load")
    catalog = LazyLoadPage(page)
    catalog.expect_loaded()
    catalog.expect_item(0, "Sauce Labs Bike Light", "$9.99")
    catalog.reveal_item(11)
    catalog.expect_item(11, "Test.allTheThings() T-Shirt (Red) (S)", "$15.99")
    capture_page("lazy-load")
