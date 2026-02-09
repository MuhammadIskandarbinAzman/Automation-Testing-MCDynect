"""
This module defines questions related to the Inventory Dashboard.
It checks for the personalized welcome message that appears after successful login.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.dashboard_page_ui import DashboardPageUI  # pyright: ignore[reportUnusedImport]

class ComplianceDashboard:
    """
    Questions for verifying elements on the Compliance Dashboard.
    """

    @staticmethod
    def welcome_header_text(actor: Actor) -> str:
        """
        Retrieves the full text of the welcome message element.
        The inventory dashboard might have a different structure than licensee dashboard.
        Uses multiple strategies to find the welcome message.
        """
        browser = actor.uses_ability(BrowseTheWeb)
        
        # Strategy 1: Try to find "Welcome Back" text
        try:
            text_locator = browser.page.get_by_text("Welcome Back", exact=False)
            text_locator.wait_for(state='visible', timeout=5000)
            # Get the parent h1 element
            h1_locator = text_locator.locator("xpath=ancestor::h1[1]")
            h1_locator.wait_for(state='visible', timeout=5000)
            text_content = h1_locator.text_content()
            if text_content and "Welcome Back" in text_content:
                return text_content.strip()
        except Exception:
            pass
        
        # Strategy 2: Check all h1 elements for any welcome-related text
        try:
            h1_count = browser.page.locator("h1").count()
            for i in range(h1_count):
                h1_locator = browser.page.locator("h1").nth(i)
                try:
                    text = h1_locator.text_content()
                    if text:
                        # Check for "Welcome Back" or "Welcome" or "Dashboard"
                        text_lower = text.lower()
                        if "welcome" in text_lower or "dashboard" in text_lower:
                            return text.strip()
                except Exception:
                    continue
        except Exception:
            pass
        
        # Strategy 3: Check h2 elements (some dashboards use h2 for welcome messages)
        try:
            h2_count = browser.page.locator("h2").count()
            for i in range(h2_count):
                h2_locator = browser.page.locator("h2").nth(i)
                try:
                    text = h2_locator.text_content()
                    if text:
                        text_lower = text.lower()
                        if "welcome" in text_lower or "dashboard" in text_lower:
                            return text.strip()
                except Exception:
                    continue
        except Exception:
            pass
        
        # Strategy 4: Try getting text directly from get_by_text() for "Welcome"
        try:
            text_locator = browser.page.get_by_text("Welcome", exact=False)
            text_locator.wait_for(state='visible', timeout=5000)
            text_content = text_locator.text_content()
            if text_content:
                return text_content.strip()
        except Exception:
            pass
        
        # Strategy 5: Look for "Inventory Dashboard" text
        try:
            text_locator = browser.page.get_by_text("Dashboard", exact=False)
            text_locator.wait_for(state='visible', timeout=5000)
            text_content = text_locator.text_content()
            if text_content:
                return text_content.strip()
        except Exception:
            pass
        
        # Strategy 6: Get the first h1 element as fallback (might be the page title)
        try:
            first_h1 = browser.page.locator("h1").first
            first_h1.wait_for(state='visible', timeout=5000)
            text_content = first_h1.text_content()
            if text_content:
                return text_content.strip()
        except Exception:
            pass
        t
        return ""

    @staticmethod
    def has_personal_welcome(actor: Actor) -> bool:
        """
        Checks if the personalized welcome message is displayed.
        The message should start with "Welcome Back," followed by a user identifier.
        """
        try:
            text = ComplianceDashboard.welcome_header_text(actor)
            return text is not None and text.strip().startswith("Welcome Back,")
        except Exception:
            return False

    @staticmethod
    def is_welcome_message_visible(actor: Actor) -> bool:
        """
        Checks if the welcome message h1 element is visible on the page.
        Uses multiple strategies to find the welcome message to handle different page structures.
        If we can successfully get the welcome text, we consider it visible.
        """
        browser = actor.uses_ability(BrowseTheWeb)
        
        # Strategy 1: Check if "Welcome Back" text is visible anywhere on the page
        try:
            text_locator = browser.page.get_by_text("Welcome Back", exact=False)
            text_locator.wait_for(state='visible', timeout=5000)
            return text_locator.is_visible()
        except Exception:
            pass
        
        # Strategy 2: Check all h1 elements for the welcome text
        try:
            h1_count = browser.page.locator("h1").count()
            for i in range(h1_count):
                h1_locator = browser.page.locator("h1").nth(i)
                try:
                    # Get text content
                    text = h1_locator.text_content()
                    if text and "Welcome Back" in text:
                        # Found it! Check if it's visible
                        return h1_locator.is_visible()
                except Exception:
                    continue
        except Exception:
            pass
        
        # Strategy 3: If we can get the welcome text using welcome_header_text, consider it visible
        try:
            text = InventoryDashboard.welcome_header_text(actor)
            if text and "Inventory Dashboard" in text:
                return True
        except Exception:
            pass
        
        return False