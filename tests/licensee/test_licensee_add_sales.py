import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

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
def test_MCD_LCSE_15_add_sales_open_form(the_licensee):
    """
    Use Case: MCD-LCSE-15
    Verifies Licensee can open Add Sale page from Sales dashboard and see required fields.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    # Navigate to Sales page from sidebar or fallback direct URL.
    sales_menu = page.locator("aside a:has-text('Sales'), aside button:has-text('Sales')").first
    if sales_menu.count() > 0 and sales_menu.is_visible():
        sales_menu.click()
    else:
        page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")

    try:
        page.wait_for_url("**/licensee/sales**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        assert "/licensee/sales" in page.url, f"Unexpected sales URL: {page.url}"

    add_sale_btn = page.locator("button:has-text('Add sale'), a:has-text('Add sale')").first
    expect(add_sale_btn).to_be_visible()
    add_sale_btn.click()

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    # Add Sale form checks (non-destructive).
    expect(page.locator("text=/Add\\s*Sale/i").first).to_be_visible()
    expect(page.locator("text=/Date/i").first).to_be_visible()
    expect(page.locator("text=/KG\\s*sold/i").first).to_be_visible()
    expect(page.locator("text=/Cash/i").first).to_be_visible()
    expect(page.locator("text=/Online\\s*\\(QR\\)/i").first).to_be_visible()
    expect(page.locator("text=/GrabFood/i").first).to_be_visible()
    expect(page.locator("text=/ShopeeFood/i").first).to_be_visible()
    expect(page.locator("text=/Foodpanda/i").first).to_be_visible()
    expect(page.locator("text=/Misi\\s*Delivery/i").first).to_be_visible()
    expect(page.locator("text=/Haloje/i").first).to_be_visible()
    expect(page.locator("text=/Set\\s*the\\s*day\\s*as\\s*closed|Key\\s*in\\s*sale/i").first).to_be_visible()
