import pytest
from playwright.sync_api import expect

from actors.licensee import Licensee
from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL, LOGIN_CREDENTIALS
from tasks.login import Login


@pytest.mark.licensee
def test_MCD_LCSE_04_access_redeemable_item_tab_shortcut(the_licensee: Licensee):
    """
    Use Case: MCD-LCSE-04
    Verifies Licensee can click the "Redeem" shortcut from home page
    and is redirected to the redeemable item tab in order page.
    """
    creds = LOGIN_CREDENTIALS["licensee"]
    the_licensee.attempts_to(
        Login.with_credentials(creds["email"], creds["password"]),
    )

    page = the_licensee.uses_ability(BrowseTheWeb).page
    page.locator("button:has-text('Redeem')").first.click()
    page.wait_for_url("**/licensee/order/index?tab=redeemable", timeout=15000)

    expect(page).to_have_url(f"{BASE_URL}/licensee/order/index?tab=redeemable")
    expect(page.locator("h1:has-text('Order Stock')").first).to_be_visible()
