import os

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login


def _resolve_sales_creds() -> dict:
    switch_email = os.getenv("MCDYNECT_SWITCH_OUTLET_EMAIL", "").strip()
    switch_password = os.getenv("MCDYNECT_SWITCH_OUTLET_PASSWORD", "").strip()
    if switch_email and switch_password:
        return {"email": switch_email, "password": switch_password}
    return LOGIN_CREDENTIALS["licensee"]


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
def test_MCD_LCSE_19_add_extra_sets_sales_open_form(the_licensee):
    """
    Use Case: MCD-LCSE-19
    Verifies Licensee can open Add Extra Sets Sale page from Sales screen.
    Non-destructive: validates form visibility only.
    """
    creds = _resolve_sales_creds()
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)
    _open_sales_page(page)

    extra_sets_tabs = page.locator(
        "button:has-text('Extra Sets'), [role='tab']:has-text('Extra Sets'), a:has-text('Extra Sets')"
    )
    visible_extra_tabs = [
        i for i in range(extra_sets_tabs.count()) if extra_sets_tabs.nth(i).is_visible()
    ]
    if not visible_extra_tabs:
        pytest.skip("Extra Sets tab is not available for current outlet/account.")
    extra_sets_tabs.nth(visible_extra_tabs[0]).click()

    add_extra_btn = page.locator(
        "button:has-text('Add Extra'), a:has-text('Add Extra'), "
        "button:has-text('Add extra'), a:has-text('Add extra')"
    )
    visible_add_extra = [
        i for i in range(add_extra_btn.count()) if add_extra_btn.nth(i).is_visible()
    ]
    if not visible_add_extra:
        pytest.skip("Add Extra Sets Sale action is not available in current environment.")
    add_extra_btn.nth(visible_add_extra[0]).click()

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    expect(page.locator("text=/Add\\s*.*Extra|Add\\s*sale/i").first).to_be_visible()
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
