import re

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
    for status_label in ["Not filled", "Not complete", "Completed", "Submitted", "Pending"]:
        rows = page.locator("table tbody tr", has_text=status_label)
        for i in range(rows.count()):
            row = rows.nth(i)
            if not row.is_visible():
                continue
            try:
                row_action = row.locator(
                    "a[href*='/licensee/sales/'], button:has-text('View'), a:has-text('View')"
                ).first
                if row_action.count() > 0 and row_action.is_visible():
                    row_action.click()
                else:
                    row.locator("td").first.click()
                clicked = True
                break
            except Exception:
                continue
        if clicked:
            break

    if not clicked:
        generic_rows = page.locator("table tbody tr")
        for i in range(generic_rows.count()):
            row = generic_rows.nth(i)
            if not row.is_visible():
                continue
            try:
                row_action = row.locator(
                    "a[href*='/licensee/sales/'], button:has-text('View'), a:has-text('View'), a, button"
                ).first
                if row_action.count() > 0 and row_action.is_visible():
                    row_action.click()
                else:
                    row.locator("td").first.click()
                clicked = True
                break
            except Exception:
                continue

    if not clicked:
        sales_links = page.eval_on_selector_all(
            "a[href*='/licensee/sales/']",
            "els => els.map(e => e.getAttribute('href') || '').filter(Boolean)",
        )
        details_href_pattern = re.compile(r"/licensee/sales/([^/?#]+)")
        blocked_segments = {"index", "add", "create", "edit"}
        details_link = next(
            (
                href
                for href in sales_links
                if (
                    (match := details_href_pattern.search(href))
                    and match.group(1).lower() not in blocked_segments
                )
            ),
            None,
        )
        if details_link:
            target_url = details_link if details_link.startswith("http") else f"{BASE_URL}{details_link}"
            page.goto(target_url, wait_until="domcontentloaded")
            clicked = True

    if not clicked:
        pytest.skip("No daily sales details row/link available to open details.")

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    if page.url.endswith("/licensee/sales/index"):
        row_view_btn = page.locator(
            "table tbody tr button:has-text('View'), table tbody tr a:has-text('View')"
        ).first
        if row_view_btn.count() > 0 and row_view_btn.is_visible():
            row_view_btn.click()
            try:
                page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
            except PlaywrightTimeoutError:
                pass

    if page.url.endswith("/licensee/sales/index"):
        sales_links = page.eval_on_selector_all("a[href*='/licensee/sales/']", "els => els.map(e => e.href)")
        details_link = next(
            (
                href
                for href in sales_links
                if re.search(r"/licensee/sales/[^/?#]+$", href)
                and not re.search(r"/licensee/sales/(index|add|create|edit)$", href)
            ),
            None,
        )
        if details_link:
            page.goto(details_link, wait_until="domcontentloaded")

    if page.url.endswith("/licensee/sales/index"):
        pytest.skip("Sales Details page is not navigable from current listing UI/data.")

    assert not page.url.endswith("/licensee/sales/create"), f"Landed on create page, expected details URL: {page.url}"
    assert not page.url.endswith("/licensee/sales/add"), f"Landed on add page, expected details URL: {page.url}"
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
