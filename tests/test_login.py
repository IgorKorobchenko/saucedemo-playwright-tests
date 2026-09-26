import pytest

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.manual_script("MT-001")
def test_valid_login(login, page):
    login.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.manual_script("MT-003")
@pytest.mark.parametrize("username,password,message", [
    ("", "", "Epic sadface: Username is required"),
    ("", "secret_sauce", "Epic sadface: Username is required"),
    ("standard_user", "", "Epic sadface: Password is required"),
])
def test_required_fields_and_recovery(login, page, username, password, message):
    login.login(username, password)
    login.expect_error(message)
    login.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


@pytest.mark.p1
@pytest.mark.manual_script("MT-004")
@pytest.mark.parametrize("username,password,message", [
    ("standard_user", "wrong", "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
])
def test_rejected_login_and_recovery(login, page, username, password, message):
    login.login(username, password)
    login.expect_error(message)
    login.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


@pytest.mark.p2
@pytest.mark.manual_script("MT-005")
@pytest.mark.parametrize("username,password", [
    (" standard_user ", "secret_sauce"),
    ("standard_user", " secret_sauce "),
])
def test_surrounding_whitespace_is_not_trimmed(login, page, username, password):
    """Observed baseline; no unsupported maximum-length or format rule asserted."""
    login.login(username, password)
    login.expect_error("Epic sadface: Username and password do not match any user in this service")
    login.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


@pytest.mark.p2
@pytest.mark.coverage_gap("G03")
@pytest.mark.manual_script("MT-004")
@pytest.mark.parametrize("password", ["secret_sauce", "BABBA"], ids=["unknown-user", "both-invalid"])
def test_unknown_username_is_rejected_with_recovery(login, page, password):
    login.login("ABBA", password)
    login.expect_error("Epic sadface: Username and password do not match any user in this service")
    login.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()
