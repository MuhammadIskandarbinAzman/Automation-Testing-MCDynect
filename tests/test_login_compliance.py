from actors.compliance import Compliance

from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login


def test_compliance_can_log_in(the_compliance: Compliance):
    from abilities.browse_the_web import BrowseTheWeb
    from questions.inventory_dashboard import InventoryDashboard

    credentials = LOGIN_CREDENTIALS["compliance"]
    the_compliance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )

    browser = the_compliance.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=10000)
    browser.page.wait_for_load_state("networkidle", timeout=10000)
    browser.page.wait_for_timeout(10000)

    assert CurrentURL.value_for(the_compliance) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_compliance)}"
    )

    welcome_text = InventoryDashboard.welcome_header_text(the_compliance)
    assert welcome_text, "Welcome message not found on the dashboard!"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )
