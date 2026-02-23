import pytest
from playwright.sync_api import expect

from actors.licensee import Licensee
from abilities.browse_the_web import BrowseTheWeb
from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login
from tasks.logout import Logout
from ui.login_page_ui import LoginPageUI


@pytest.mark.licensee
def test_MCD_LCSE_03_logout_basic_path_from_user_menu(the_licensee: Licensee):
    creds = LOGIN_CREDENTIALS["licensee"]
    browser = the_licensee.uses_ability(BrowseTheWeb)
    the_licensee.attempts_to(
        Login.with_credentials(creds["email"], creds["password"]),
    )
    try:
        browser.page.wait_for_url(creds["expected_dashboard_url"], timeout=10000)
    except Exception:
        browser.page.goto(creds["expected_dashboard_url"])
        browser.page.wait_for_url(creds["expected_dashboard_url"], timeout=10000)
    the_licensee.attempts_to(Logout.from_user_menu())

    page = browser.page
    expect(page.locator(LoginPageUI.EMAIL_FIELD).first).to_be_visible()
    assert "/login" in CurrentURL.value_for(the_licensee)
