"""
This module contains Pytest fixtures for setting up the Playwright browser, page, and Actors.
These fixtures ensure a clean and consistent state for each test.
"""
import pathlib
import os
import sys
import pytest
from datetime import datetime
from playwright.sync_api import Page, sync_playwright
from playwright._impl._errors import TargetClosedError

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
# Ensure local packages (abilities, actors, tasks, questions) are importable.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
    # Use project root to keep artifacts under this repo.
    base_dir = pathlib.Path(__file__).parent.resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create a unique output folder per test session.
    test_output_dir = os.path.join(base_dir, "test_runs", timestamp)
    os.makedirs(test_output_dir, exist_ok=True)
    # Store on config so hooks/fixtures can access it.
    config.test_output_dir = test_output_dir


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that captures screenshots after each test execution.
    Screenshots are saved in the session-specific output directory.
    """
    # Let pytest run the test first, then inspect the result.
    outcome = yield
    rep = outcome.get_result()

    # Only proceed if we're in the "call" phase (actual test execution)
    # Only capture screenshots for the test body, not setup/teardown.
    if rep.when != "call":
        return

    # Get Playwright page if available
    # Look up the Playwright page fixture if this test uses it.
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
    # Use the session-scoped output directory created in pytest_configure.
    test_output_dir = item.config.test_output_dir
    screenshots_dir = os.path.join(test_output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate safe filename from test nodeid
    # Make a filesystem-safe test name for screenshot files.
    safe_test_name = (
        rep.nodeid
        .replace("/", "_")
        .replace("::", "__")
        .replace(".py", "")
        .replace(" ", "_")
    )
    # Put screenshots in a per-test subfolder under the session screenshots dir.
    test_screenshots_dir = os.path.join(screenshots_dir, safe_test_name)
    os.makedirs(test_screenshots_dir, exist_ok=True)
    base_path = os.path.join(test_screenshots_dir, safe_test_name)

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
        print(
            f"⚠️ Skipping screenshot for {safe_test_name} - TargetClosedError (page closed)"
        )
    except Exception as e:
        print(f"⚠️ Screenshot error for {safe_test_name}: {type(e).__name__}: {e}")


@pytest.fixture(scope="session")
def playwright_browser():
    """
    Provides a Playwright browser instance for the entire test session.
    Set `headless=False` to see the browser UI during tests (useful for debugging).
    """
    # Read runtime options from env for CI/local toggles.
    headless_env = os.getenv("MCDYNECT_HEADLESS", "false").strip().lower()
    headless = headless_env in {"1", "true", "yes", "y"}
    browser_name = os.getenv("MCDYNECT_BROWSER", "chromium").strip().lower()
    launch_env = dict(os.environ)
    # Reduce Crashpad noise and permission errors on macOS.
    launch_env["PLAYWRIGHT_DISABLE_CRASH_REPORTER"] = "1"
    pw_home = ROOT_DIR / ".pw_home"
    pw_home.mkdir(exist_ok=True)
    # Force browser HOME to a writable repo-local directory.
    launch_env["HOME"] = str(pw_home)
    with sync_playwright() as p:
        # Map env selection to Playwright browser type.
        if browser_name == "firefox":
            browser_type = p.firefox
        elif browser_name == "webkit":
            browser_type = p.webkit
        else:
            browser_type = p.chromium

        browser = browser_type.launch(
            headless=headless,
            args=[
                "--disable-crash-reporter",
                "--disable-crashpad",
            ],
            env=launch_env,
        )
        yield browser
        # Always close the shared browser at session end.
        browser.close()


@pytest.fixture(scope="function")
def page(playwright_browser):
    """
    Provides a new Playwright Page instance for each test function.
    """
    # Create a fresh page per test to avoid state leaks.
    page = playwright_browser.new_page()
    yield page
    # Ensure pages are closed even if tests fail.
    page.close()


# --- Actor Fixtures ---
# Each fixture initializes a specific Actor and grants them the BrowseTheWeb ability.
# This allows tests to simply request `the_licensee` (or `the_area_manager`, etc.)
# without needing to set up the actor in every test.

from config.credentials import LOGIN_CREDENTIALS


@pytest.fixture(scope="function")
def the_licensee(page: Page) -> Licensee:
    creds = LOGIN_CREDENTIALS["licensee"]
    # Store credentials on the actor so tasks can access them.
    actor = Licensee(
        email=creds["email"],
        password=creds["password"],
    )
    actor.current_password = creds.get("current_password", creds["password"])
    # Grant the browser ability used by tasks and questions.
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


# --- How to add a new Actor Fixture ---
# 1. Ensure the Actor class is defined in `actors/` and imported here.
# 2. Add a new fixture function:
#    `@pytest.fixture(scope="function")`
#    `def the_new_actor_role(page: Page) -> NewActorRole:`
#        `return NewActorRole().who_can(BrowseTheWeb.with_browser_page(page))`
#    (Replace `NewActorRole` with your actual actor class name).
