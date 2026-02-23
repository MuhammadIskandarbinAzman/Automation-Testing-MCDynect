import os

import pytest
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from ui.login_page_ui import LoginPageUI


def _get_uc_activities_credentials() -> tuple[str, str]:
    email = os.getenv("MCDYNECT_SWITCH_OUTLET_EMAIL", "").strip()
    password = os.getenv("MCDYNECT_SWITCH_OUTLET_PASSWORD", "").strip()
    if not email or not password:
        raise RuntimeError(
            "UC12/UC13 require MCDYNECT_SWITCH_OUTLET_EMAIL and "
            "MCDYNECT_SWITCH_OUTLET_PASSWORD in .env"
        )
    return email, password


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


@pytest.mark.licensee
def test_MCD_LCSE_12_view_licensee_activities_form_application(the_licensee):
    """
    Use Case: MCD-LCSE-12
    Verifies Licensee can view activities application listing and open form details modal.
    """
    browser = the_licensee.uses_ability(BrowseTheWeb)
    page = browser.page
    email, password = _get_uc_activities_credentials()

    browser.clear_session()
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, email)
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, password)
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    page.wait_for_url("**/licensee/dashboard", timeout=15000)
    _dismiss_maybe_later_if_present(page)

    # In dashboard this is the 3rd visible "See more" and routes to application-form page.
    see_more_buttons = page.locator("button:has-text('See more'), a:has-text('See more')")
    visible_indexes = [
        i for i in range(see_more_buttons.count()) if see_more_buttons.nth(i).is_visible()
    ]
    assert len(visible_indexes) >= 3, "Could not find Activities section 'See more' shortcut."
    see_more_buttons.nth(visible_indexes[2]).click()

    page.wait_for_url("**/licensee/application-form/index", timeout=15000)
    expect(page.locator("text=/Licensee activities form application/i").first).to_be_visible()

    view_btn = page.locator("button:has-text('View')").first
    if view_btn.count() == 0 or not view_btn.is_visible():
        empty_state = page.locator("text=/don't have any pending application currently/i").first
        expect(empty_state).to_be_visible()
        pytest.skip("No existing application available to open in Form Details modal.")
    view_btn.click()

    modal_title = page.locator("text=/Form Details/i").first
    expect(modal_title).to_be_visible()
    expect(page.locator("text=/EVN-/i").first).to_be_visible()
    page.locator("button:has-text('Close')").first.click()
    expect(modal_title).not_to_be_visible()


@pytest.mark.licensee
def test_MCD_LCSE_13_create_licensee_activities_form_application(the_licensee):
    """
    Use Case: MCD-LCSE-13
    Verifies Licensee can open Create Application modal and navigate to selected application form.
    """
    browser = the_licensee.uses_ability(BrowseTheWeb)
    page = browser.page
    email, password = _get_uc_activities_credentials()

    browser.clear_session()
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, email)
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, password)
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    page.wait_for_url("**/licensee/dashboard", timeout=15000)
    _dismiss_maybe_later_if_present(page)

    page.goto(f"{BASE_URL}/licensee/application-form/index")
    page.wait_for_load_state("domcontentloaded", timeout=10000)

    create_btn = page.locator("button:has-text('Create application')").first
    expect(create_btn).to_be_visible()
    create_btn.click()

    modal_title = page.locator("text=Select the application type").first
    expect(modal_title).to_be_visible()

    # Choose one listed type and verify redirect to corresponding form page.
    page.locator("a:has-text('Event participant')").first.click()
    page.wait_for_url("**/licensee/application-form/event/index", timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/licensee/application-form/event/index")
