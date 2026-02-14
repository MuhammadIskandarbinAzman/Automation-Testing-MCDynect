import pytest
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login


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
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    see_all_btn = page.locator(
        "button:has-text('See all announcements'), a:has-text('See all announcements')"
    ).first
    expect(see_all_btn).to_be_visible()
    see_all_btn.click()

    page.wait_for_url("**/licensee/announcement/index", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/licensee/announcement/index")

    announcement_link = page.locator("a[target='_blank']").first
    expect(announcement_link).to_be_visible()

    with page.expect_popup(timeout=10000) as popup_info:
        announcement_link.click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded", timeout=10000)

    assert popup.url.startswith("http"), "Announcement detail did not open as a valid link."
    popup.close()
