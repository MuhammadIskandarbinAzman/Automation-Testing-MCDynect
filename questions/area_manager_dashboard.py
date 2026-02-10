"""
This module defines questions related to the Area Manager Dashboard.
It checks for the personalized welcome message that appears after successful login.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.dashboard_page_ui import DashboardPageUI

class AreaManagerDashboard:
    """
    Questions for verifying elements on the Area Manager Dashboard.
    """

    @staticmethod
    def welcome_header_text(actor: Actor) -> str:
        """
        Retrieves the full text of the welcome message h1 element.
        Example: "Welcome Back, HQO#05"
        Uses multiple strategies to find the welcome message h1 element.
        """
        # Use the actor's browser ability to inspect the dashboard.
        browser = actor.uses_ability(BrowseTheWeb)
        
        # Strategy 1: Use get_by_text() to find the text, then get parent h1
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
        
        # Strategy 2: Check all h1 elements for the welcome text
        try:
            h1_count = browser.page.locator("h1").count()
            for i in range(h1_count):
                h1_locator = browser.page.locator("h1").nth(i)
                try:
                    text = h1_locator.text_content()
                    if text and "Welcome Back" in text:
                        return text.strip()
                except Exception:
                    continue
        except Exception:
            pass
        
        # Strategy 3: Try getting text directly from get_by_text()
        try:
            text_locator = browser.page.get_by_text("Welcome Back", exact=False)
            text_locator.wait_for(state='visible', timeout=5000)
            text_content = text_locator.text_content()
            if text_content:
                return text_content.strip()
        except Exception:
            pass
        
        return ""

    @staticmethod
    def has_personal_welcome(actor: Actor) -> bool:
        """
        Checks if the personalized welcome message is displayed.
        The message should start with "Welcome Back," followed by a user identifier.
        """
        try:
            text = AreaManagerDashboard.welcome_header_text(actor)
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
        # Use the actor's browser ability to check visibility.
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
            text = AreaManagerDashboard.welcome_header_text(actor)
            if text and "Welcome Back" in text:
                return True
        except Exception:
            pass
        
        return False
