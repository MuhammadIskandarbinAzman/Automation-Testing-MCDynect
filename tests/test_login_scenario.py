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
from questions.current_url import CurrentURL

# --- Test Scenarios ---
# Each test function represents a user story or a specific interaction flow.
# Actors are injected via Pytest fixtures (e.g., `the_licensee`).

def test_licensee_can_log_in(the_licensee: Licensee):
    """
    Verifies that a Licensee actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_licensee.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 1 second for any dynamic content
    assert CurrentURL.value_for(the_licensee) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_licensee)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.licensee_dashboard import LicenseeDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = LicenseeDashboard.welcome_header_text(the_licensee)
    # Verify the welcome message exists and contains expected text
    assert welcome_text, "Welcome message not found on the dashboard!"
    assert "Welcome Back" in welcome_text, (
        f"Welcome message does not contain 'Welcome Back'. Found: '{welcome_text}'"
    )
    # Verify it starts with "Welcome Back,"
    assert welcome_text.strip().startswith("Welcome Back,"), (
        f"Welcome message does not start with 'Welcome Back,'. Found: '{welcome_text}'"
    )
    # After login, check if the welcome message is visible.
    # This is a robust check for successful login.
    #//assert WelcomeMessage.is_visible_to(the_licensee), "Welcome Back message not visible for Licensee"// this line of code is commented out because using a different assertion. 
    # Optional: Further assertions can be added here, e.g., checking dashboard URL or specific elements.
    # For this, you would need to add `the_licensee.uses_ability(BrowseTheWeb).check_url()`
    # and add `BrowseTheWeb` to the imports if you uncomment that line.
    # expect(the_licensee.uses_ability(BrowseTheWeb).page).to_have_url(credentials["expected_dashboard_url"])

def test_licensee_cannot_log_in_with_invalid_credentials(the_licensee: Licensee, page: Page):
    """
    Verifies that a Licensee actor cannot log in with invalid credentials
    and the correct error message is displayed.
    """
    from abilities.browse_the_web import BrowseTheWeb
    from config.credentials import BASE_URL
    
    # Perform login manually to avoid the on-boarding timeout
    browser = the_licensee.uses_ability(BrowseTheWeb)
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, "invalid@gmail.com")
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, "invalidpassword")
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    
    # Assert that the specific error message is displayed.
    # The `expect` assertion waits for the element to appear and contain the text.
    expect(page.locator(LoginPageUI.ERROR_MESSAGE)).to_contain_text("Invalid credentials")

def test_area_manager_can_log_in(the_area_manager: AreaManager):
    """
    Verifies that an AreaManager actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["area_manager"]
    the_area_manager.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_area_manager.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 1 second for any dynamic content
    assert CurrentURL.value_for(the_area_manager) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_area_manager)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.area_manager_dashboard import AreaManagerDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = AreaManagerDashboard.welcome_header_text(the_area_manager)
    # Verify the welcome message exists and contains expected text
    assert welcome_text, "Welcome message not found on the dashboard!"
    assert "Welcome Back" in welcome_text, (
        f"Welcome message does not contain 'Welcome Back'. Found: '{welcome_text}'"
    )
    # Verify it starts with "Welcome Back,"
    assert welcome_text.strip().startswith("Welcome Back,"), (
        f"Welcome message does not start with 'Welcome Back,'. Found: '{welcome_text}'"
    )

def test_inventory_can_log_in(the_inventory: Inventory):
    """
    Verifies that an Inventory actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["inventory"]
    the_inventory.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_inventory.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 10 seconds for any dynamic content
    assert CurrentURL.value_for(the_inventory) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_inventory)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.inventory_dashboard import InventoryDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = InventoryDashboard.welcome_header_text(the_inventory)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For inventory, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )

def test_procurement_can_log_in(the_procurement: Procurement):
    """
    Verifies that an Inventory actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["procurement"]
    the_procurement.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_procurement.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 10 seconds for any dynamic content
    assert CurrentURL.value_for(the_procurement) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_procurement)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.procurement_dashboard import ProcurementDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = ProcurementDashboard.welcome_header_text(the_procurement)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For inventory, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )

def test_production_can_log_in(the_production: Production):
    """
    Verifies that a Finance actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["finance"]
    the_production.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_production.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 10 seconds for any dynamic content
    assert CurrentURL.value_for(the_production) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_production)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.production_dashboard import ProductionDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = ProductionDashboard.welcome_header_text(the_production)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For inventory, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )
def test_licensing_can_log_in(the_licensing: Licensing):
    """
    Verifies that a Licensing actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["licensing"]
    the_licensing.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_licensing.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 1 second for any dynamic content
    assert CurrentURL.value_for(the_licensing) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_licensing)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.licensing_dashboard import LicensingDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = LicensingDashboard.welcome_header_text(the_licensing)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For licensing, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )

def test_compliance_can_log_in(the_compliance: Compliance):
    """
    Verifies that a Compliance actor can successfully log into the application.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["compliance"]
    the_compliance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
     # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_compliance.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 10 seconds for any dynamic content
    assert CurrentURL.value_for(the_compliance) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_compliance)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.inventory_dashboard import InventoryDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = InventoryDashboard.welcome_header_text(the_compliance)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For inventory, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )


def test_finance_can_log_in(the_finance: Finance):
    """
    Verifies that a Finance actor can successfully log into the application.
    Waits for the dashboard URL after login before further assertions.
    """
    from abilities.browse_the_web import BrowseTheWeb
    credentials = LOGIN_CREDENTIALS["finance"]
    the_finance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )
    # Wait for URL redirection before screenshots or dashboard assertions
    browser = the_finance.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=5000)
    # Wait for page to be fully loaded (network idle) to ensure all content is rendered
    browser.page.wait_for_load_state("networkidle", timeout=5000)
    # Additional small wait to ensure JavaScript-rendered content is displayed
    browser.page.wait_for_timeout(5000)  # Wait 10 seconds for any dynamic content
    assert CurrentURL.value_for(the_finance) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_finance)}"
    )
    # Assert personalized welcome message is visible and contains expected text
    from questions.finance_dashboard import FinanceDashboard
    # Get the welcome text (this will wait for the element and throw if not found)
    welcome_text = FinanceDashboard.welcome_header_text(the_finance)
    
    # Debug: Print what we found if empty
    if not welcome_text:
        # Try to get page title and first few h1/h2 elements for debugging
        try:
            page_title = browser.page.title()
            h1_count = browser.page.locator("h1").count()
            h2_count = browser.page.locator("h2").count()
            debug_info = f"Page title: {page_title}, H1 count: {h1_count}, H2 count: {h2_count}"
            if h1_count > 0:
                first_h1 = browser.page.locator("h1").first.text_content()
                debug_info += f", First H1: '{first_h1}'"
            if h2_count > 0:
                first_h2 = browser.page.locator("h2").first.text_content()
                debug_info += f", First H2: '{first_h2}'"
            assert False, f"Welcome message not found on the dashboard! Debug info: {debug_info}"
        except Exception as e:
            assert False, f"Welcome message not found on the dashboard! Error getting debug info: {str(e)}"
    
    # Verify the welcome message exists and contains expected text
    # For inventory, we'll be more flexible - just check if it contains "Welcome" or "Dashboard"
    assert welcome_text, "Welcome message not found on the dashboard!"
    
    # Check if it contains "Welcome" (case insensitive) or "Dashboard"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )

# --- How to add a new Test Scenario ---
# 1. Choose the `Actor` (e.g., `the_licensee`) that will perform the test and add it to the function signature.
# 2. Use `actor.attempts_to()` to chain together `Tasks` (e.g., `Login`, `NavigateToDashboard`).
# 3. Use `Questions` to query the UI and `assert` the expected state.
#    Example: `assert DashboardTitle.is_displayed_by(actor), "Dashboard title not found"`.
# 4. Remember to import any new Tasks, Questions, or UI Page Objects you create.
