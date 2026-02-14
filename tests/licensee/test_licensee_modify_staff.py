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


def _open_first_staff_edit_modal(page):
    edit_btn = page.locator("button:has-text('Edit')").first
    if edit_btn.count() == 0:
        edit_btn = page.get_by_text("edit", exact=True).first
    expect(edit_btn).to_be_visible()
    edit_btn.click()
    modal_title = page.locator("text=Edit staff").first
    expect(modal_title).to_be_visible()
    return modal_title.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")


@pytest.mark.licensee
def test_MCD_LCSE_10_modify_staff_information(the_licensee):
    """
    Use Case: MCD-LCSE-10
    Modifies staff name in Edit Staff form, verifies update, then restores original value.
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
    page.goto(f"{BASE_URL}/licensee/staff/index")
    page.wait_for_load_state("domcontentloaded", timeout=10000)

    modal = _open_first_staff_edit_modal(page)
    name_input = modal.locator("input").first
    expect(name_input).to_be_visible()

    original_name = name_input.input_value().strip()
    modified_name = (
        f"{original_name} QA"
        if not original_name.endswith(" QA")
        else f"{original_name} X"
    )
    start_date_input = modal.locator("input[type='date']").first

    name_input.fill(modified_name)
    # Some accounts require start date for successful update.
    if start_date_input.count() > 0 and not start_date_input.input_value().strip():
        start_date_input.fill("2026-02-12")

    modal.locator("button:has-text('Update staff')").first.click()
    expect(page.locator("text=Edit staff").first).not_to_be_visible()
    expect(page.locator(f"text={modified_name}").first).to_be_visible()

    # Revert for test data stability.
    modal = _open_first_staff_edit_modal(page)
    modal.locator("input").first.fill(original_name)
    revert_date_input = modal.locator("input[type='date']").first
    if revert_date_input.count() > 0 and not revert_date_input.input_value().strip():
        revert_date_input.fill("2026-02-12")
    modal.locator("button:has-text('Update staff')").first.click()
    expect(page.locator("text=Edit staff").first).not_to_be_visible()
    expect(page.locator(f"text={original_name}").first).to_be_visible()
