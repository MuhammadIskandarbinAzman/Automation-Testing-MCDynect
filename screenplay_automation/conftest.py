import pytest
from playwright.sync_api import Page, sync_playwright

from abilities.browse_the_web import BrowseTheWeb
from actors.base_actor import Actor
from actors.licensee import Licensee
from actors.area_manager import AreaManager
from actors.inventory import Inventory
from actors.procurement import Procurement
from actors.production import Production
from actors.licensing import Licensing
from actors.compliance import Compliance
from actors.finance import Finance

@pytest.fixture(scope="session")
def playwright_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_browser):
    page = playwright_browser.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def the_licensee(page: Page) -> Licensee:
    return Licensee().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_area_manager(page: Page) -> AreaManager:
    return AreaManager().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_inventory(page: Page) -> Inventory:
    return Inventory().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_procurement(page: Page) -> Procurement:
    return Procurement().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_production(page: Page) -> Production:
    return Production().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_licensing(page: Page) -> Licensing:
    return Licensing().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_compliance(page: Page) -> Compliance:
    return Compliance().who_can(BrowseTheWeb.with_browser_page(page))

@pytest.fixture(scope="function")
def the_finance(page: Page) -> Finance:
    return Finance().who_can(BrowseTheWeb.with_browser_page(page))

