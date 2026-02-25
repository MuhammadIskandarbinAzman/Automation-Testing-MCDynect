import os
import re

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
    # Grab credentials modal appears intermittently after login.
    # Try a few times so it doesn't block subsequent clicks.
    for _ in range(6):
        maybe_later = page.locator(
            "button:has-text('Maybe Later'), button:has-text('Maybe later')"
        ).first
        if maybe_later.count() > 0 and maybe_later.is_visible():
            try:
                maybe_later.click()
            except Exception:
                maybe_later.click(force=True)
            page.wait_for_timeout(300)
            return
        page.wait_for_timeout(500)


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


def _open_sales_details_page_or_fail(page) -> None:
    def _is_valid_details_url(url: str) -> bool:
        # Most stable indicator for this app's details page.
        if "/licensee/sales/show/" in url:
            return True
        return (
            "/licensee/sales/" in url
            and not url.endswith("/licensee/sales/index")
            and not re.search(r"/licensee/sales/(add|create|edit)$", url)
            and "/licensee/sales/extra/" not in url
        )

    if _is_valid_details_url(page.url):
        return

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
        # Non-table layout fallback: click visible status labels in list rows.
        for status_label in ["Not complete", "Completed", "Submitted", "Pending", "Not filled"]:
            status_items = page.locator(f"text={status_label}")
            for i in range(status_items.count()):
                item = status_items.nth(i)
                if not item.is_visible():
                    continue
                try:
                    item.click()
                except Exception:
                    continue
                page.wait_for_timeout(500)
                try:
                    page.wait_for_url("**/licensee/sales/**", timeout=4000, wait_until="domcontentloaded")
                except PlaywrightTimeoutError:
                    pass
                if _is_valid_details_url(page.url):
                    clicked = True
                    break
                # If we landed on add/create/extra path, return to listing and continue trying.
                if page.url != f"{BASE_URL}/licensee/sales/index":
                    page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")
            if clicked:
                break

    if not clicked:
        sales_links = page.eval_on_selector_all(
            "a[href*='/licensee/sales/']",
            "els => els.map(e => e.getAttribute('href') || '').filter(Boolean)",
        )
        details_link = next(
            (
                href
                for href in sales_links
                if re.search(r"/licensee/sales/[^/?#]+$", href)
                and not re.search(r"/licensee/sales/(index|add|create|edit)$", href)
                and "/licensee/sales/extra/" not in href
            ),
            None,
        )
        if details_link:
            target_url = details_link if details_link.startswith("http") else f"{BASE_URL}{details_link}"
            page.goto(target_url, wait_until="domcontentloaded")
            clicked = True

    # Final guard: if we're already on a valid details page, continue.
    if _is_valid_details_url(page.url):
        return

    if not clicked:
        raise AssertionError("No daily sales details row/link available to open details.")

    try:
        page.wait_for_url(
            "**/licensee/sales/**",
            timeout=15000,
            wait_until="domcontentloaded",
        )
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
                and "/licensee/sales/extra/" not in href
            ),
            None,
        )
        if details_link:
            page.goto(details_link, wait_until="domcontentloaded")

    if not _is_valid_details_url(page.url):
        raise AssertionError("Sales Details page is not navigable from current listing UI/data.")


def _try_open_details_with_delete(page) -> bool:
    delete_btn = page.locator("button:has-text('Delete'), a:has-text('Delete')").first
    if delete_btn.count() > 0 and delete_btn.is_visible():
        return True

    sales_links = page.eval_on_selector_all("a[href*='/licensee/sales/']", "els => els.map(e => e.href)")
    candidate_links = [
        href
        for href in sales_links
        if re.search(r"/licensee/sales/[^/?#]+$", href)
        and not re.search(r"/licensee/sales/(index|add|create|edit)$", href)
        and "/licensee/sales/extra/" not in href
    ]
    seen = set()
    for href in candidate_links:
        if href in seen:
            continue
        seen.add(href)
        page.goto(href, wait_until="domcontentloaded")
        delete_btn = page.locator("button:has-text('Delete'), a:has-text('Delete')").first
        if delete_btn.count() > 0 and delete_btn.is_visible():
            return True
    return False


@pytest.mark.licensee
def test_MCD_LCSE_18_delete_daily_sales_record(the_licensee):
    """
    Use Case: MCD-LCSE-18
    Verifies Delete Sales Record modal flow from Sales Details page.
    By default this test is safe-mode (cancel delete).
    Set MCDYNECT_RUN_DESTRUCTIVE_UC18=true to execute real deletion.
    """
    creds = _resolve_sales_creds()
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)
    _open_sales_page(page)
    _open_sales_details_page_or_fail(page)

    assert _try_open_details_with_delete(page), (
        "Delete action is not available for current sales record."
    )

    delete_btn = page.locator("button:has-text('Delete'), a:has-text('Delete')").first

    details_url_before_delete = page.url
    delete_btn.click()

    modal_title = page.locator(
        "text=/Delete\\s*Sales\\s*Record|You\\s*are\\s*deleting\\s*this\\s*sale\\s*record/i"
    ).first
    expect(modal_title).to_be_visible()

    destructive_mode = os.getenv("MCDYNECT_RUN_DESTRUCTIVE_UC18", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
    }

    if not destructive_mode:
        cancel_btn = page.locator("button:has-text('Cancel'), button:has-text('Close')").first
        if cancel_btn.count() > 0 and cancel_btn.is_visible():
            cancel_btn.click()
            expect(modal_title).not_to_be_visible()
        else:
            page.keyboard.press("Escape")
        return

    # Destructive path (opt-in only).
    confirm_delete_btn = page.locator("button:has-text('Delete')").last
    expect(confirm_delete_btn).to_be_visible()
    confirm_delete_btn.click()

    try:
        page.wait_for_url("**/licensee/sales/index", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    assert page.url.endswith("/licensee/sales/index"), (
        f"Expected redirect back to sales listing after delete. Before={details_url_before_delete}, "
        f"After={page.url}"
    )
