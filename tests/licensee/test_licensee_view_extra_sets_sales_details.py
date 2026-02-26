import os
import re
from datetime import date, timedelta

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from ui.login_page_ui import LoginPageUI


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


def _ensure_target_outlet_if_configured(page) -> None:
    target_outlet = os.getenv("MCDYNECT_SWITCH_OUTLET_TARGET", "Cyberjaya").strip()
    if not target_outlet:
        return

    card = page.locator("text=Outlet Account Switcher").first.locator(
        "xpath=ancestor::div[contains(@class,'rounded')][1]"
    )
    if card.count() == 0 or not card.first.is_visible():
        return

    current_rows = card.locator("div.flex.justify-between.px-2").filter(
        has=page.locator("button p:has-text('Current')")
    )
    if current_rows.count() > 0:
        current_name = current_rows.first.locator("p.text-grey-800").first.inner_text().strip().lower()
        if target_outlet.lower() in current_name:
            return

    target_rows = card.locator("div.flex.justify-between.px-2").filter(
        has=page.locator(f"p.text-grey-800:has-text('{target_outlet}')")
    )
    for i in range(target_rows.count()):
        row = target_rows.nth(i)
        switch_btn = row.locator("button p:has-text('Switch')")
        if switch_btn.count() > 0:
            row.locator("button").first.click()
            page.wait_for_timeout(1500)
            return


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
    page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    for attempt in range(3):
        _dismiss_maybe_later_if_present(page)
        extra_sets_tabs = page.get_by_role("tab", name=re.compile(r"^Extra\s*sets$", re.I))
        visible_tabs = [i for i in range(extra_sets_tabs.count()) if extra_sets_tabs.nth(i).is_visible()]

        if not visible_tabs:
            exact_buttons = page.locator("button").filter(has_text=re.compile(r"^Extra\s*sets$", re.I))
            visible_tabs = [i for i in range(exact_buttons.count()) if exact_buttons.nth(i).is_visible()]
            if visible_tabs:
                tab = exact_buttons.nth(visible_tabs[0])
            else:
                tab = None
        else:
            tab = extra_sets_tabs.nth(visible_tabs[0])

        if tab:
            tab.click(force=True, timeout=5000)
            page.wait_for_timeout(1200)
            if "/licensee/sales/index" in page.url:
                return
            return
        if attempt < 2:
            page.goto(f"{BASE_URL}/licensee/sales/index", wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
    pytest.skip("Extra Sets tab is not available for current outlet/account.")



def _open_extra_sets_details_or_skip(page) -> bool:
    def _valid_details_url(url: str) -> bool:
        return bool(
            ("/licensee/sales/extra/" in url and not re.search(r"/licensee/sales/extra/(index|add|create|edit)$", url))
            or ("/licensee/sales/show/" in url)
        )

    if _valid_details_url(page.url):
        return True

    show_links = page.locator("a[href*='/licensee/sales/show/']")
    if show_links.count() == 0:
        return False

    # Prefer visible row link; fallback to direct navigation by href.
    for i in range(show_links.count()):
        link = show_links.nth(i)
        try:
            href = link.get_attribute("href") or ""
        except Exception:
            href = ""
        if not href or not re.search(r"/licensee/sales/show/[^/?#]+", href):
            continue
        target_url = href if href.startswith("http") else f"{BASE_URL}{href}"
        try:
            page.goto(target_url, wait_until="domcontentloaded")
            break
        except Exception:
            continue

    try:
        page.wait_for_url("**/licensee/sales/**", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass

    return _valid_details_url(page.url)

def _seed_extra_sets_sale(page) -> None:
    # Seed a minimal extra-sets sale record so UC20 can open details deterministically.
    page.goto(f"{BASE_URL}/licensee/sales/extra/create", wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    _dismiss_maybe_later_if_present(page)

    seed_date = (date.today() - timedelta(days=60)).isoformat()
    page.fill("input[type='date']", seed_date)
    page.fill("#kg-sold", "12")
    page.fill("#cash", "100")
    page.fill("#online", "20")

    key_in_sale = page.locator("button:has-text('Key in sale')").first
    expect(key_in_sale).to_be_visible()
    key_in_sale.click()

    try:
        page.wait_for_url("**/licensee/sales/index", timeout=15000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        pass


@pytest.mark.licensee
def test_MCD_LCSE_20_view_extra_sets_sales_details(the_licensee):
    """
    Use Case: MCD-LCSE-20
    Verifies Licensee can open and view Extra Sets sales details.
    """
    creds = _resolve_sales_creds()
    browser = the_licensee.uses_ability(BrowseTheWeb)
    page = browser.page
    browser.clear_session()
    browser.go_to(f"{BASE_URL}/login")
    browser.find_and_fill(LoginPageUI.EMAIL_FIELD, creds["email"])
    browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, creds["password"])
    browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
    page.wait_for_url("**/licensee/dashboard", timeout=20000)

    _dismiss_maybe_later_if_present(page)
    _ensure_target_outlet_if_configured(page)
    _dismiss_maybe_later_if_present(page)
    _open_sales_page(page)
    _open_extra_sets_tab(page)
    opened = _open_extra_sets_details_or_skip(page)
    if not opened:
        _seed_extra_sets_sale(page)
        _open_sales_page(page)
        _open_extra_sets_tab(page)
        opened = _open_extra_sets_details_or_skip(page)
    assert opened, "Unable to open Extra Sets sales details page after deterministic seed step."

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
