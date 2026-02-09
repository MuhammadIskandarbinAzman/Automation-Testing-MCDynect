"""
This module contains Pytest fixtures for setting up the Playwright browser, page, and Actors.
These fixtures ensure a clean and consistent state for each test.
"""
import pathlib
import os
import pytest
from datetime import datetime
from playwright.sync_api import Page, sync_playwright
from playwright._impl._errors import TargetClosedError  # ← ADDED AT TOP

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

def pytest_configure(config):
    """
    Called once at test session startup.
    Creates a timestamped output directory and attaches it to config.
    """
    base_dir = pathlib.Path(__file__).parent.resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_output_dir = os.path.join(base_dir, "test_runs", timestamp)
    os.makedirs(test_output_dir, exist_ok=True)
    config.test_output_dir = test_output_dir  
    # Make it globally accessible

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that captures screenshots after each test execution.
    Screenshots are saved in the session-specific output directory.
    """
    outcome = yield
    rep = outcome.get_result()

    # Only proceed if we're in the "call" phase (actual test execution)
    if rep.when != "call":
        return

    # Get Playwright page if available
    page = item.funcargs.get("page", None)
    if page is None:
        return

    # CRITICAL FIX: Check if page is still open BEFORE attempting screenshot
    try:
        if page.is_closed():
            print(f"⚠️ Skipping screenshot - page already closed for {rep.nodeid}")
            return
    except Exception as e:
        print(f"⚠️ Error checking page state: {e}")
        return

    # Get the session-wide output directory created in pytest_configure
    test_output_dir = item.config.test_output_dir
    screenshots_dir = os.path.join(test_output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate safe filename from test nodeid
    safe_test_name = (
        rep.nodeid
        .replace("/", "_")
        .replace("::", "__")
        .replace(".py", "")
        .replace(" ", "_")
    )
    base_path = os.path.join(screenshots_dir, safe_test_name)

    try:
        # Wait for page stability before screenshot
        page.wait_for_load_state("networkidle", timeout=5000)
        
        # Take screenshot on pass or fail
        if rep.failed:
            page.screenshot(path=f"{base_path}__FAILED.png", full_page=True)
            print(f"📸 Screenshot saved: {base_path}__FAILED.png")
        elif rep.passed:
            page.screenshot(path=f"{base_path}__PASSED.png", full_page=True)
            print(f"📸 Screenshot saved: {base_path}__PASSED.png")
            
    except TargetClosedError:
        print(f"⚠️ Skipping screenshot for {safe_test_name} - TargetClosedError (page closed)")
    except Exception as e:
        print(f"⚠️ Screenshot error for {safe_test_name}: {type(e).__name__}: {e}")

@pytest.fixture(scope="session")
def playwright_browser():
    """
    Provides a Playwright browser instance for the entire test session.
    Set `headless=False` to see the browser UI during tests (useful for debugging).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_browser):
    """
    Provides a new Playwright Page instance for each test function.
    """
    page = playwright_browser.new_page()
    yield page
    page.close()

# --- Actor Fixtures ---
# Each fixture initializes a specific Actor and grants them the BrowseTheWeb ability.
# This allows tests to simply request `the_licensee` (or `the_area_manager`, etc.)
# without needing to set up the actor in every test.

from config.credentials import LOGIN_CREDENTIALS

@pytest.fixture(scope="function")
def the_licensee(page: Page) -> Licensee:
    creds = LOGIN_CREDENTIALS["licensee"]
    actor = Licensee(
        email=creds["email"],
        password=creds["password"]
    )
    actor.who_can(BrowseTheWeb.with_browser_page(page))
    return actor

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