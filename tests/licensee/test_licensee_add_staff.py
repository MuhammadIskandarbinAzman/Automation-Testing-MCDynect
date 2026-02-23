import os
import time
from datetime import date

import pytest
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from ui.login_page_ui import LoginPageUI


def _get_uc_staff_credentials() -> tuple[str, str]:
    email = os.getenv("MCDYNECT_SWITCH_OUTLET_EMAIL", "").strip()
    password = os.getenv("MCDYNECT_SWITCH_OUTLET_PASSWORD", "").strip()
    if email and password:
        return email, password

    # Fallback to standard licensee credentials when dedicated account is not set.
    creds = LOGIN_CREDENTIALS["licensee"]
    return creds["email"], creds["password"]


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


@pytest.mark.licensee
def test_MCD_LCSE_11_add_staff(the_licensee):
    """
    Use Case: MCD-LCSE-11
    Verifies Licensee can add a new staff from Staff Directory page.
    """
    browser = the_licensee.uses_ability(BrowseTheWeb)
    page = browser.page
    email, password = _get_uc_staff_credentials()

    browser.clear_session()
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, email)
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, password)
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    page.wait_for_url("**/licensee/dashboard", timeout=15000)

    _dismiss_maybe_later_if_present(page)

    page.goto(f"{BASE_URL}/licensee/staff/index")
    page.wait_for_load_state("domcontentloaded", timeout=10000)

    page.locator("button:has-text('Add Staff')").first.click()

    modal = page.locator("text=Add New Staff").first.locator(
        "xpath=ancestor::div[contains(@class,'rounded')][1]"
    )
    expect(modal).to_be_visible()

    staff_name = f"QA Auto {int(time.time())}"
    staff_phone = f"01{int(time.time()) % 100000000:08d}"

    modal.locator("input[placeholder*='name' i]").first.fill(staff_name)
    modal.locator("input[placeholder*='phone' i]").first.fill(staff_phone)

    start_date = modal.locator("input[type='date']").first
    if start_date.count() > 0:
        start_date.fill(date.today().isoformat())

    modal.locator("button:has-text('Add New Staff')").first.click()

    expect(page.locator("text=Add New Staff").first).not_to_be_visible()
    expect(page.locator(f"text={staff_name}").first).to_be_visible()
