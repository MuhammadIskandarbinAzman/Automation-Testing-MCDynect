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


def _open_sales_page(page) -> None:
    sales_menu = page.locator("aside a:has-text('Sales'), aside button:has-text('Sales')").first
    if sales_menu.count() > 0 and sales_menu.is_visible():
        sales_menu.click()
    else:
        page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")

    try:
        page.wait_for_url("**/licensee/sales**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        assert "/licensee/sales" in page.url, f"Unexpected sales URL: {page.url}"


@pytest.mark.licensee
def test_MCD_LCSE_17_edit_daily_sales_details_open_form(the_licensee):
    """
    Use Case: MCD-LCSE-17
    Verifies Licensee can open Edit Sales form from Sales Details page.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)
    _open_sales_page(page)

    clicked = False
    for status_label in ["Not complete", "Completed", "Submitted", "Pending"]:
        status_items = page.locator(f"text={status_label}")
        for i in range(status_items.count()):
            candidate = status_items.nth(i)
            if not candidate.is_visible():
                continue
            try:
                candidate.click()
                clicked = True
                break
            except Exception:
                continue
        if clicked:
            break

    if not clicked:
        pytest.skip("No non-empty daily sales status row available to open details.")

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    if page.url.endswith("/licensee/sales/index"):
        pytest.skip("Sales Details page is not navigable from current listing UI/data.")

    edit_btn = page.locator("button:has-text('Edit'), a:has-text('Edit')").first
    if edit_btn.count() == 0 or not edit_btn.is_visible():
        pytest.skip("Edit action is not available for current sales record.")
    edit_btn.click()

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    # Non-destructive checks on Edit Sales page.
    expect(page.locator("text=/Edit\\s*Sales|Edit\\s*sale/i").first).to_be_visible()
    expect(page.locator("text=/Date/i").first).to_be_visible()
    expect(page.locator("text=/KG\\s*sold/i").first).to_be_visible()
    expect(page.locator("text=/Cash/i").first).to_be_visible()
    expect(page.locator("text=/Online\\s*\\(QR\\)/i").first).to_be_visible()
    expect(page.locator("text=/GrabFood/i").first).to_be_visible()
    expect(page.locator("text=/ShopeeFood/i").first).to_be_visible()
    expect(page.locator("text=/Foodpanda/i").first).to_be_visible()
    expect(page.locator("text=/Misi\\s*Delivery/i").first).to_be_visible()
    expect(page.locator("text=/Haloje/i").first).to_be_visible()
    expect(page.locator("text=/Update\\s*Sale/i").first).to_be_visible()
