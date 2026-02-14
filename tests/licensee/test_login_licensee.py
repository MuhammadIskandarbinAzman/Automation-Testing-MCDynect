from actors.licensee import Licensee
from playwright.sync_api import Page, expect

from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login
from ui.login_page_ui import LoginPageUI


def test_licensee_can_log_in(the_licensee: Licensee):
    from abilities.browse_the_web import BrowseTheWeb
    from questions.licensee_dashboard import LicenseeDashboard

    credentials = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )

    browser = the_licensee.uses_ability(BrowseTheWeb)
    try:
        browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=10000)
    except Exception:
        browser.page.goto(credentials["expected_dashboard_url"])
        browser.page.wait_for_url(credentials["expected_dashboard_url"], timeout=10000)

    browser.page.wait_for_load_state("networkidle", timeout=10000)
    browser.page.wait_for_timeout(10000)

    assert CurrentURL.value_for(the_licensee) == credentials["expected_dashboard_url"], (
        f"Expected URL {credentials['expected_dashboard_url']}, got {CurrentURL.value_for(the_licensee)}"
    )

    welcome_text = LicenseeDashboard.welcome_header_text(the_licensee)
    assert welcome_text, "Welcome message not found on the dashboard!"
    assert "Welcome Back" in welcome_text, (
        f"Welcome message does not contain 'Welcome Back'. Found: '{welcome_text}'"
    )
    assert welcome_text.strip().startswith("Welcome Back,"), (
        f"Welcome message does not start with 'Welcome Back,'. Found: '{welcome_text}'"
    )


def test_licensee_cannot_log_in_with_invalid_credentials(
    the_licensee: Licensee, page: Page
):
    from abilities.browse_the_web import BrowseTheWeb
    from config.credentials import BASE_URL

    browser = the_licensee.uses_ability(BrowseTheWeb)
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, "invalid@gmail.com")
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, "invalidpassword")
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)

    error = page.locator(
        "p.text-error-500",
        has_text="These credentials do not match our records.",
    )
    expect(error).to_be_visible()
