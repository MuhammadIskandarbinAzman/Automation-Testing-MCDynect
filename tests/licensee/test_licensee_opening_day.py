import time

import pytest
from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import LOGIN_CREDENTIALS
from tasks.login import Login


def _dismiss_maybe_later_if_present(page) -> None:
    maybe_later = page.locator("button:has-text('Maybe Later')")
    if maybe_later.count() > 0 and maybe_later.first.is_visible():
        maybe_later.first.click()


def _opening_day_card(page):
    card = page.locator("text=Opening Day").first.locator(
        "xpath=ancestor::div[contains(@class,'rounded')][1]"
    )
    expect(card).to_be_visible()
    return card


def _ensure_licensee_dashboard(actor, creds) -> None:
    """Retry login once if session drops back to /login before opening-day checks."""
    page = actor.uses_ability(BrowseTheWeb).page
    if "/login" in page.url:
        actor.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
        page = actor.uses_ability(BrowseTheWeb).page
    try:
        page.wait_for_url("**/licensee/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        # Keep proceeding and let downstream assertions fail with clearer UI context.
        pass


def _get_visible_day_row(card, day: str):
    rows = card.locator("div.flex.items-center.justify-between").filter(
        has=card.page.locator(f"p:has-text('{day}')")
    )
    for i in range(rows.count()):
        row = rows.nth(i)
        if row.is_visible():
            return row
    raise AssertionError(f"Could not find visible opening-day row for {day}.")


def _get_status_text(day_row) -> str:
    status_btn = day_row.locator(
        "button:has(p:has-text('Open')), button:has(p:has-text('Closed'))"
    ).first
    return status_btn.inner_text().strip()


def _wait_for_status(day_row, expected: str, timeout_sec: int = 15) -> None:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if _get_status_text(day_row) == expected:
            return
        day_row.page.wait_for_timeout(500)
    raise AssertionError(f"Opening-day status did not change to '{expected}' in time.")


@pytest.mark.licensee
def test_MCD_LCSE_07_modify_outlet_opening_day(the_licensee):
    """
    Use Case: MCD-LCSE-07 (Basic Path)
    - Toggle day Open/Close status.
    - Open edit opening hours modal and save.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))

    _ensure_licensee_dashboard(the_licensee, creds)
    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    card = _opening_day_card(page)
    monday_row = _get_visible_day_row(card, "Monday")

    status_before = _get_status_text(monday_row)
    monday_row.locator(
        "button:has(p:has-text('Open')), button:has(p:has-text('Closed'))"
    ).first.click()

    expected_after_toggle = "Open" if status_before == "Closed" else "Closed"
    _wait_for_status(monday_row, expected_after_toggle)

    # Revert to original status to keep test data stable.
    monday_row.locator(
        "button:has(p:has-text('Open')), button:has(p:has-text('Closed'))"
    ).first.click()
    _wait_for_status(monday_row, status_before)

    monday_row.locator("button[title='Edit opening hours']").first.click()
    modal_title = page.locator("text=/Edit Opening Hours for/i").first
    expect(modal_title).to_be_visible()

    page.locator("button:has-text('Save')").first.click()
    expect(modal_title).not_to_be_visible()


@pytest.mark.licensee
def test_MCD_LCSE_07_cancel_edit_opening_hours(the_licensee):
    """
    Use Case: MCD-LCSE-07 (Exception Path E1)
    - Open edit opening hours modal.
    - Cancel and ensure modal closes.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))

    _ensure_licensee_dashboard(the_licensee, creds)
    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)

    card = _opening_day_card(page)
    monday_row = _get_visible_day_row(card, "Monday")
    monday_row.locator("button[title='Edit opening hours']").first.click()

    modal_title = page.locator("text=/Edit Opening Hours for/i").first
    expect(modal_title).to_be_visible()

    page.locator("button:has-text('Cancel')").first.click()
    expect(modal_title).not_to_be_visible()
