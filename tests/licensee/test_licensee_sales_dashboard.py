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


def _open_sales_from_sidebar(page) -> None:
    sales_menu = page.locator(
        "aside a:has-text('Sales'), aside button:has-text('Sales')"
    ).first
    if sales_menu.count() > 0 and sales_menu.is_visible():
        sales_menu.click()
    else:
        page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")

    try:
        page.wait_for_url("**/licensee/sales**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        assert "/licensee/sales" in page.url, f"Unexpected sales URL: {page.url}"


@pytest.mark.licensee
def test_MCD_LCSE_14_view_sales_dashboard(the_licensee):
    """
    Use Case: MCD-LCSE-14
    Verifies Licensee can access Sales page and view Daily Sales/Extra Sets tabs.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))

    _ensure_licensee_dashboard(the_licensee, creds)
    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)
    _open_sales_from_sidebar(page)

    # Sales dashboard shell.
    sales_header = page.locator("h1:has-text('Sales')").first
    if sales_header.count() > 0 and sales_header.is_visible():
        expect(sales_header).to_be_visible()
    else:
        expect(page.get_by_text("Sales Dashboard", exact=False).first).to_be_visible()

    # Daily Sales tab and listing.
    daily_tab = page.locator(
        "button:has-text('Daily sales'), [role='tab']:has-text('Daily sales'), a:has-text('Daily sales')"
    ).first
    expect(daily_tab).to_be_visible()
    daily_tab.click()
    expect(page.locator("text=/\\d{4}-\\d{2}-\\d{2}/").first).to_be_visible()
    expect(page.locator("text=/Not\\s*filled|Submitted|Pending/i").first).to_be_visible()

    # Extra Sets tab exists and is accessible (feature may be disabled for some outlets).
    extra_sets_tabs = page.locator(
        "button:has-text('Extra Sets'), [role='tab']:has-text('Extra Sets'), a:has-text('Extra Sets')"
    )
    visible_extra_sets = [
        i for i in range(extra_sets_tabs.count()) if extra_sets_tabs.nth(i).is_visible()
    ]
    if visible_extra_sets:
        extra_sets_tabs.nth(visible_extra_sets[0]).click()
        expect(page.locator("text=/Extra\\s*Sets|\\d{4}-\\d{2}-\\d{2}/i").first).to_be_visible()
