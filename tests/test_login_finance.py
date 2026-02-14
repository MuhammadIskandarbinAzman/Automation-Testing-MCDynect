from actors.finance import Finance

from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login


def test_finance_can_log_in(the_finance: Finance):
    from abilities.browse_the_web import BrowseTheWeb
    from questions.finance_dashboard import FinanceDashboard

    credentials = LOGIN_CREDENTIALS["finance"]
    the_finance.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )

    browser = the_finance.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=10000)
    browser.page.wait_for_load_state("networkidle", timeout=10000)
    browser.page.wait_for_timeout(10000)

    assert CurrentURL.value_for(the_finance) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_finance)}"
    )

    welcome_text = FinanceDashboard.welcome_header_text(the_finance)
    assert welcome_text, "Welcome message not found on the dashboard!"
    welcome_lower = welcome_text.lower()
    assert "welcome" in welcome_lower or "dashboard" in welcome_lower, (
        f"Welcome message does not contain 'Welcome' or 'Dashboard'. Found: '{welcome_text}'"
    )
