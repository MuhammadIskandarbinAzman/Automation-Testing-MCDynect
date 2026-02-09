"""
This module defines the BrowseTheWeb ability, which allows actors to interact with web pages using Playwright.
"""
from playwright.sync_api import Page, Locator

class BrowseTheWeb:
    """
    An ability that allows an Actor to browse the web using a Playwright Page instance.
    It encapsulates direct Playwright interactions.
    """
    def __init__(self, page: Page):
        # Keep the Playwright Page instance to drive UI interactions.
        self.page = page

    @staticmethod
    def with_browser_page(page: Page) -> "BrowseTheWeb":
        """
        Instantiates the BrowseTheWeb ability with a Playwright Page.
        This is typically used in Pytest fixtures (see `conftest.py`).
        """
        # Factory to keep call sites clean in fixtures and tests.
        return BrowseTheWeb(page)

    def go_to(self, url: str) -> None:
        """
        Navigates the browser to the specified URL.
        """
        # Navigate to the target URL.
        self.page.goto(url)
    
    def clear_session(self) -> None:
        """
        Clears cookies and web storage for a clean authentication state.
        """
        # Clear cookies at the browser context level.
        self.page.context.clear_cookies()
        # Clear local/session storage for the current origin.
        self.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")

    def find_and_fill(self, locator: str, value: str) -> None:
        """
        Finds an element by locator and fills it with the given value.
        """
        # Locate the element and fill with the given value.
        self.page.locator(locator).fill(value)

    def find_and_click(self, locator: str) -> None:
        """
        Finds an element by locator and clicks it.
        """
        # Locate the element and click it.
        self.page.locator(locator).click()

    def find_element(self, locator: str) -> Locator:
        """
        Finds an element by locator and returns its Locator object.
        Useful for assertions with Playwright's `expect`.
        """
        # Expose the raw Locator for advanced assertions.
        return self.page.locator(locator)

    def find_text_content(self, locator: str) -> str:
        """
        Finds an element by locator and returns its text content.
        """
        # Ensure the element is visible before trying to get text content
        # Wait for visibility so text_content is stable.
        locator_obj = self.page.locator(locator)
        locator_obj.wait_for(state='visible')
        return locator_obj.text_content()

    def find_and_check_visibility(self, locator: str) -> bool:
        """
        Checks if an element is visible on the page.
        """
        # Return visibility state for quick assertions.
        return self.page.locator(locator).is_visible()

    def check_url(self) -> str:
        """
        Returns the current URL of the page.
        """
        # Provide the current browser URL.
        return self.page.url

# --- How to add a new Ability ---
# 1. Create a new file in this directory (e.g., `call_an_api.py`).
# 2. Define a class (e.g., `CallAnAPI`) that encapsulates interactions with an API client.
# 3. Add a `@staticmethod` factory method (e.g., `CallAnAPI.using_client(api_client)`).
# 4. Actors can then use `.who_can(CallAnAPI.using_client(some_client))`.
# 5. Tasks and Questions can access this ability via `actor.uses_ability(CallAnAPI)`.
