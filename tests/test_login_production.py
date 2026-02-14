from actors.production import Production

from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login


def test_production_can_log_in(the_production: Production):
    from abilities.browse_the_web import BrowseTheWeb
    from questions.production_dashboard import ProductionDashboard

    credentials = LOGIN_CREDENTIALS["production"]
    the_production.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )

    browser = the_production.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=10000)
    browser.page.wait_for_load_state("networkidle", timeout=10000)
    browser.page.wait_for_timeout(10000)

    assert CurrentURL.value_for(the_production) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_production)}"
    )

    welcome_text = ProductionDashboard.welcome_header_text(the_production)
    assert welcome_text, "Welcome message not found on the dashboard!"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )
