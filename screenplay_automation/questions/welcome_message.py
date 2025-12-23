"""
This module defines the WelcomeMessage question.
Questions are how an Actor inspects the state of the system.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb

class WelcomeMessage:
    """
    A question to determine if the 'Welcome Back' message is visible or to retrieve its text.
    """
    @staticmethod
    def is_visible_to(actor: Actor) -> bool:
        """
        Checks if the 'Welcome Back' message is visible to the actor.
        """
        browser = actor.uses_ability(BrowseTheWeb)
        return browser.find_and_check_visibility("text=Welcome Back")

    @staticmethod
    def text_for(actor: Actor) -> str:
        """
        Retrieves the text content of the 'Welcome Back' message for the actor.
        """
        browser = actor.uses_ability(BrowseTheWeb)
        return browser.find_text_content("text=Welcome Back")

# --- How to create a new Question ---
# 1. Create a new file in this directory (e.g., `dashboard_title.py`).
# 2. Define a class (e.g., `DashboardTitle`).
# 3. Implement `@staticmethod` methods to formulate the question:
#    - `displayed_by(actor: Actor) -> str`: To get the text content of an element.
#    - `is_displayed_by(actor: Actor) -> bool`: To check visibility of an element.
# 4. In these methods, get the `BrowseTheWeb` ability: `browser = actor.uses_ability(BrowseTheWeb)`.
# 5. Use `browser` methods and relevant UI locators (e.g., `DashboardPageUI.TITLE`) to answer the question.

