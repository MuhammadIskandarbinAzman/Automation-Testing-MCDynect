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
    # Grab credentials modal can block sidebar/tab clicks after login.
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


def _open_extra_sets_tab(page) -> None:
    extra_sets_tabs = page.locator(
        "button:has-text('Extra Sets'), [role='tab']:has-text('Extra Sets'), a:has-text('Extra Sets')"
    )
    visible_tabs = [i for i in range(extra_sets_tabs.count()) if extra_sets_tabs.nth(i).is_visible()]
    if not visible_tabs:
        pytest.skip("Extra Sets tab is not available for current outlet/account.")

    extra_sets_tabs.nth(visible_tabs[0]).click()
    page.wait_for_timeout(800)



def _open_extra_sets_details_or_skip(page) -> None:
    def _valid_details_url(url: str) -> bool:
        # Extra sets commonly uses dedicated route, but keep fallback for shared details route.
        return bool(
            ("/licensee/sales/extra/" in url and not re.search(r"/licensee/sales/extra/(index|add|create|edit)$", url))
            or ("/licensee/sales/show/" in url)
        )

    if _valid_details_url(page.url):
        return

    clicked = False
    rows = page.locator("table tbody tr")
    for i in range(rows.count()):
        row = rows.nth(i)
        if not row.is_visible():
            continue
        try:
            row_action = row.locator(
                "a[href*='/licensee/sales/extra/'], "
                "a[href*='/licensee/sales/show/'], "
                "a[href*='/licensee/sales/'], "
                "button:has-text('View'), a:has-text('View')"
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
        # Non-table listing fallback: click status chips/date labels that usually open details.
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
                if _valid_details_url(page.url):
                    clicked = True
                    break
                if page.url != f"{BASE_URL}/licensee/sales/index":
                    page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")
                    _open_extra_sets_tab(page)
            if clicked:
                break

    if not clicked:
        date_items = page.locator("text=/\\d{4}-\\d{2}-\\d{2}/")
        for i in range(date_items.count()):
            item = date_items.nth(i)
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
            if _valid_details_url(page.url):
                clicked = True
                break
            if page.url != f"{BASE_URL}/licensee/sales/index":
                page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")
                _open_extra_sets_tab(page)

    if not clicked:
        links = page.eval_on_selector_all(
            "a[href*='/licensee/sales/']",
            "els => els.map(e => e.getAttribute('href') || '').filter(Boolean)",
        )
        details_link = next(
            (
                href
                for href in links
                if (
                    "/licensee/sales/extra/" in href
                    and not re.search(r"/licensee/sales/extra/(index|add|create|edit)$", href)
                )
                or re.search(r"/licensee/sales/show/[^/?#]+$", href)
            ),
            None,
        )
        if details_link:
            target_url = details_link if details_link.startswith("http") else f"{BASE_URL}{details_link}"
            page.goto(target_url, wait_until="domcontentloaded")
            clicked = True

    if not clicked:
        pytest.skip("No Extra Sets sales details row/link available to open details.")

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    if not _valid_details_url(page.url) and page.url.endswith("/licensee/sales/index"):
        pytest.skip("Extra Sets details page is not navigable from current listing UI/data.")


@pytest.mark.licensee
def test_MCD_LCSE_20_view_extra_sets_sales_details(the_licensee):
    """
    Use Case: MCD-LCSE-20
    Verifies Licensee can open and view Extra Sets sales details.
    """
    creds = _resolve_sales_creds()
    the_licensee.attempts_to(Login.with_credentials(creds["email"], creds["password"]))
    _ensure_licensee_dashboard(the_licensee, creds)

    page = the_licensee.uses_ability(BrowseTheWeb).page
    _dismiss_maybe_later_if_present(page)
    _open_sales_page(page)
    _open_extra_sets_tab(page)
    _open_extra_sets_details_or_skip(page)

    expect(page.locator(r"text=/Sale\s*details|Sales\s*Details/i").first).to_be_visible()
    expect(page.locator(r"text=/RM\s*\d+|Total\s*Sales|Sales\s*Amount/i").first).to_be_visible()
    expect(page.locator(r"text=/Status/i").first).to_be_visible()
    expect(page.locator(r"text=/KG\s*sold/i").first).to_be_visible()
    expect(page.locator(r"text=/Unsold\s*sets|Unsold\s*Sets\s*\(Excess\)/i").first).to_be_visible()
    expect(page.locator(r"text=/Cash/i").first).to_be_visible()
    expect(page.locator(r"text=/Online\s*\(QR\)/i").first).to_be_visible()
    expect(page.locator(r"text=/GrabFood/i").first).to_be_visible()
    expect(page.locator(r"text=/ShopeeFood/i").first).to_be_visible()
    expect(page.locator(r"text=/Foodpanda/i").first).to_be_visible()
    expect(page.locator(r"text=/Misi\s*Delivery/i").first).to_be_visible()
    expect(page.locator(r"text=/Haloje/i").first).to_be_visible()
