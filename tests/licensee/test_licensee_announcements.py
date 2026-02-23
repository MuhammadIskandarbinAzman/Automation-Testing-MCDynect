import os

import pytest
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login
from ui.login_page_ui import LoginPageUI


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


@pytest.mark.licensee
def test_MCD_LCSE_08_view_all_announcement_listings_and_details(the_licensee):
    """
    Use Case: MCD-LCSE-08
    - Open full announcement listing.
    - Open one announcement detail in a new browser tab.
    """
    switch_email = os.getenv("MCDYNECT_SWITCH_OUTLET_EMAIL", "").strip()
    switch_password = os.getenv("MCDYNECT_SWITCH_OUTLET_PASSWORD", "").strip()
    creds = (
        {"email": switch_email, "password": switch_password}
        if switch_email and switch_password
        else LOGIN_CREDENTIALS["licensee"]
    )
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    see_all_btn = page.locator(
        "button:has-text('See all announcements'), a:has-text('See all announcements')"
    ).first
    if see_all_btn.count() > 0 and see_all_btn.is_visible():
        see_all_btn.click()
        page.wait_for_url("**/licensee/announcement/index", timeout=15000)
    else:
        # Fallback for sessions where dashboard section is not rendered.
        page.goto(f"{BASE_URL}/licensee/announcement/index")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
    if "/login" in page.url:
        # Session may have been redirected out; recover once and re-open announcements.
        page.fill(LoginPageUI.EMAIL_FIELD, creds["email"])
        page.fill(LoginPageUI.PASSWORD_FIELD, creds["password"])
        page.click(LoginPageUI.SIGN_IN_BUTTON)
        page.wait_for_timeout(3000)
        assert "/login" not in page.url, f"Login recovery did not leave login page: {page.url}"
        page.goto(f"{BASE_URL}/licensee/announcement/index")
    assert "/licensee/announcement/index" in page.url, f"Unexpected URL: {page.url}"
    expect(page).to_have_url(f"{BASE_URL}/licensee/announcement/index")

    announcement_link = page.locator("a[target='_blank']").first
    expect(announcement_link).to_be_visible()

    with page.expect_popup(timeout=10000) as popup_info:
        announcement_link.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded", timeout=10000)

    assert popup.url.startswith("http"), "Announcement detail did not open as a valid link."
    popup.close()
