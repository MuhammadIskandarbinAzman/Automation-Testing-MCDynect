from actors.licensee import Licensee
from actors.area_manager import AreaManager
from actors.inventory import Inventory
from actors.procurement import Procurement
from actors.production import Production
from actors.licensing import Licensing
from actors.compliance import Compliance
from actors.finance import Finance

from tasks.login import Login
from questions.welcome_message import WelcomeMessage
from playwright.sync_api import Page, expect
from ui.login_page_ui import LoginPageUI
from config.credentials import LOGIN_CREDENTIALS

def test_licensee_can_log_in(the_licensee: Licensee):
    credentials = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Assuming successful login leads to a dashboard where 'Welcome Back' is visible
    assert WelcomeMessage.is_visible_to(the_licensee), "Welcome Back message not visible for Licensee"
    # We can also assert the URL if it changes to a specific dashboard URL for the licensee
    # expect(the_licensee.uses_ability(BrowseTheWeb).check_url()).to_equal(credentials["expected_dashboard_url"])

def test_licensee_cannot_log_in_with_invalid_credentials(the_licensee: Licensee, page: Page):
    the_licensee.attempts_to(
        Login.with_credentials("invalid@gmail.com", "invalidpassword")
    )
    expect(page.locator(LoginPageUI.ERROR_MESSAGE)).to_contain_text("These credentials do not match our records.")

def test_area_manager_can_log_in(the_area_manager: AreaManager):
    credentials = LOGIN_CREDENTIALS["area_manager"]
    the_area_manager.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_area_manager), "Welcome Back message not visible for AreaManager"

def test_inventory_can_log_in(the_inventory: Inventory):
    credentials = LOGIN_CREDENTIALS["inventory"]
    the_inventory.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_inventory), "Welcome Back message not visible for Inventory"

def test_procurement_can_log_in(the_procurement: Procurement):
    credentials = LOGIN_CREDENTIALS["procurement"]
    the_procurement.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_procurement), "Welcome Back message not visible for Procurement"

def test_production_can_log_in(the_production: Production):
    credentials = LOGIN_CREDENTIALS["production"]
    the_production.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_production), "Welcome Back message not visible for Production"

def test_licensing_can_log_in(the_licensing: Licensing):
    credentials = LOGIN_CREDENTIALS["licensing"]
    the_licensing.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_licensing), "Welcome Back message not visible for Licensing"

def test_compliance_can_log_in(the_compliance: Compliance):
    credentials = LOGIN_CREDENTIALS["compliance"]
    the_compliance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_compliance), "Welcome Back message not visible for Compliance"

def test_finance_can_log_in(the_finance: Finance):
    credentials = LOGIN_CREDENTIALS["finance"]
    the_finance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_finance), "Welcome Back message not visible for Finance"
