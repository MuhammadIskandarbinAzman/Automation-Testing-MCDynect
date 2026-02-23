import pytest
from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


def _ensure_licensee_dashboard(actor, creds) -> None:
    page = actor.uses_ability(BrowseTheWeb).page
    if "/login" in page.url:
        actor.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
        page = actor.uses_ability(BrowseTheWeb).page
    try:
        page.wait_for_url("**/licensee/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass


@pytest.mark.licensee
def test_MCD_LCSE_09_view_all_staff_directory(the_licensee):
    """
    Use Case: MCD-LCSE-09
    Verifies user can open Staff Directory full listing from dashboard section.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)
    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    staff_card = page.locator("text=Staff directory").first.locator(
        "xpath=ancestor::div[contains(@class,'rounded')][1]"
    )
    expect(staff_card).to_be_visible()

    see_more_btn = staff_card.locator("button:has-text('See more'), a:has-text('See more')").first
    expect(see_more_btn).to_be_visible()
    see_more_btn.click()

    page.wait_for_url("**/licensee/staff/index", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/licensee/staff/index")
    expect(page.locator("text=/Staff Directory/i").first).to_be_visible()
