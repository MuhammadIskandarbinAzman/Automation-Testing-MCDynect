from actors.area_manager import AreaManager
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.credentials import LOGIN_CREDENTIALS
from questions.current_url import CurrentURL
from tasks.login import Login


def test_area_manager_can_log_in(the_area_manager: AreaManager):
    from abilities.browse_the_web import BrowseTheWeb
    from questions.area_manager_dashboard import AreaManagerDashboard

    credentials = LOGIN_CREDENTIALS["area_manager"]
    the_area_manager.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"])
    )

    browser = the_area_manager.uses_ability(BrowseTheWeb)
    try:
        browser.page.wait_for_url(
            credentials["expected_dashboard_url"], timeout=10000, wait_until="domcontentloaded"
        )
    except PlaywrightTimeoutError:
        # Fallback for occasional delayed/variant redirects.
        browser.page.wait_for_url("**/area-manager/**", timeout=10000, wait_until="domcontentloaded")
    browser.page.wait_for_load_state("networkidle", timeout=10000)
    browser.page.wait_for_timeout(10000)
    current_url = CurrentURL.value_for(the_area_manager)
    assert "/area-manager/" in current_url, (
        f"Expected area-manager landing URL, got {current_url}"
    )

    welcome_text = AreaManagerDashboard.welcome_header_text(the_area_manager)
    assert welcome_text, "Welcome message not found on the dashboard!"
    assert "Welcome Back" in welcome_text, (
        f"Welcome message does not contain 'Welcome Back'. Found: '{welcome_text}'"
    )
    assert welcome_text.strip().startswith("Welcome Back,"), (
        f"Welcome message does not start with 'Welcome Back,'. Found: '{welcome_text}'"
    )
