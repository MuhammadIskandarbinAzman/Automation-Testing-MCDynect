import pytest
from playwright.sync_api import expect

from actors.licensee import Licensee
from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login


@pytest.mark.licensee
def test_MCD_LCSE_05_access_trade_in_tab_page_shortcut(the_licensee: Licensee):
    """
    Use Case: MCD-LCSE-05
    Verifies Licensee can click the "Trade In" shortcut from home page
    and is redirected to the Trade In page.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(creds["email"], creds["password"]),
    )

    page = the_licensee.uses_ability(BrowseTheWeb).page
    page.locator("button:has-text('Trade In')").first.click()
    page.wait_for_url("**/licensee/trade-in", timeout=15000)

    expect(page).to_have_url(f"{BASE_URL}/licensee/trade-in")
    expect(page.locator("text=Create Trade In").first).to_be_visible()
    expect(page.locator("text=Trade In No.").first).to_be_visible()
