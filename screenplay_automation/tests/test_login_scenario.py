"""
This module contains example test scenarios for logging into the application
using the Screenplay Pattern. It demonstrates how different Actors perform Tasks
and answer Questions.
"""
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

# --- Test Scenarios ---
# Each test function represents a user story or a specific interaction flow.
# Actors are injected via Pytest fixtures (e.g., `the_licensee`).

def test_licensee_can_log_in(the_licensee: Licensee):
    """
    Verifies that a Licensee actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # After login, check if the welcome message is visible.
    # This is a robust check for successful login.
    assert WelcomeMessage.is_visible_to(the_licensee), "Welcome Back message not visible for Licensee"
    # Optional: Further assertions can be added here, e.g., checking dashboard URL or specific elements.
    # For this, you would need to add `the_licensee.uses_ability(BrowseTheWeb).check_url()`
    # and add `BrowseTheWeb` to the imports if you uncomment that line.
    # expect(the_licensee.uses_ability(BrowseTheWeb).page).to_have_url(credentials["expected_dashboard_url"])

def test_licensee_cannot_log_in_with_invalid_credentials(the_licensee: Licensee, page: Page):
    """
    Verifies that a Licensee actor cannot log in with invalid credentials
    and the correct error message is displayed.
    """
    the_licensee.attempts_to(
        Login.with_credentials("invalid@gmail.com", "invalidpassword")
    )
    # Assert that the specific error message is displayed.
    # The `expect` assertion waits for the element to appear and contain the text.
    expect(page.locator(LoginPageUI.ERROR_MESSAGE)).to_contain_text("These credentials do not match our records.")

def test_area_manager_can_log_in(the_area_manager: AreaManager):
    """
    Verifies that an AreaManager actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["area_manager"]
    the_area_manager.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_area_manager), "Welcome Back message not visible for AreaManager"

def test_inventory_can_log_in(the_inventory: Inventory):
    """
    Verifies that an Inventory actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["inventory"]
    the_inventory.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_inventory), "Welcome Back message not visible for Inventory"

def test_procurement_can_log_in(the_procurement: Procurement):
    """
    Verifies that a Procurement actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["procurement"]
    the_procurement.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_procurement), "Welcome Back message not visible for Procurement"

def test_production_can_log_in(the_production: Production):
    """
    Verifies that a Production actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["production"]
    the_production.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_production), "Welcome Back message not visible for Production"

def test_licensing_can_log_in(the_licensing: Licensing):
    """
    Verifies that a Licensing actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["licensing"]
    the_licensing.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_licensing), "Welcome Back message not visible for Licensing"

def test_compliance_can_log_in(the_compliance: Compliance):
    """
    Verifies that a Compliance actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["compliance"]
    the_compliance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_compliance), "Welcome Back message not visible for Compliance"

def test_finance_can_log_in(the_finance: Finance):
    """
    Verifies that a Finance actor can successfully log into the application.
    """
    credentials = LOGIN_CREDENTIALS["finance"]
    the_finance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    assert WelcomeMessage.is_visible_to(the_finance), "Welcome Back message not visible for Finance"

# --- How to add a new Test Scenario ---
# 1. Choose the `Actor` (e.g., `the_licensee`) that will perform the test and add it to the function signature.
# 2. Use `actor.attempts_to()` to chain together `Tasks` (e.g., `Login`, `NavigateToDashboard`).
# 3. Use `Questions` to query the UI and `assert` the expected state.
#    Example: `assert DashboardTitle.is_displayed_by(actor), "Dashboard title not found"`.
# 4. Remember to import any new Tasks, Questions, or UI Page Objects you create.
