import time

import pytest
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL
from ui.login_page_ui import LoginPageUI


TEST_LICENSEE_EMAIL = "ichiroadris@gmail.com"
TEST_LICENSEE_PASSWORD = "masterpassword1234"


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


def _get_current_outlet_name(card) -> str:
    rows = card.locator("div.flex.justify-between.px-2")
    for i in range(rows.count()):
        row = rows.nth(i)
        if row.locator("button p:has-text('Current')").count() > 0:
            return row.locator("p.text-grey-800").first.inner_text().strip()
    raise AssertionError("No outlet marked as Current in Outlet Account Switcher card.")


@pytest.mark.licensee
def test_MCD_LCSE_06_switch_outlet_account(the_licensee):
    """
    Use Case: MCD-LCSE-06
    Verifies Licensee can switch outlet from Outlet Account Switcher.
    """
    browser = the_licensee.uses_ability(BrowseTheWeb)
    page = browser.page

    browser.clear_session()
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, TEST_LICENSEE_EMAIL)
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, TEST_LICENSEE_PASSWORD)
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    page.wait_for_url("**/licensee/dashboard", timeout=15000)

    _dismiss_maybe_later_if_present(page)

    card = page.locator("text=Outlet Account Switcher").first.locator(
        "xpath=ancestor::div[contains(@class,'rounded')][1]"
    )
    expect(card).to_be_visible()

    current_before = _get_current_outlet_name(card)

    switch_rows = card.locator("div.flex.justify-between.px-2").filter(
        has=page.locator("button p:has-text('Switch')")
    )
    if switch_rows.count() == 0:
        raise AssertionError("No switchable outlet found in Outlet Account Switcher.")

    target_row = switch_rows.first
    target_outlet = target_row.locator("p.text-grey-800").first.inner_text().strip()
    target_row.locator("button").first.click()

    deadline = time.time() + 20
    while time.time() < deadline:
        if _get_current_outlet_name(card) == target_outlet:
            break
        page.wait_for_timeout(500)

    current_after = _get_current_outlet_name(card)
    assert current_after != current_before, "Outlet did not switch."
    assert current_after == target_outlet, (
        f"Expected switched outlet '{target_outlet}', got '{current_after}'."
    )
