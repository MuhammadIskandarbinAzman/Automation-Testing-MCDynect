"""
This module defines UI locators for the Dashboard Page.
It centralizes how elements are found on the dashboard, making tests resilient to UI changes.
"""
class DashboardPageUI:
    """
    Locators for elements on the dashboard page.
    """
    # Welcome message heading - appears after successful login
    # HTML: <h1 class="">Welcome Back, L23#304</h1>
    # Using text matching to avoid strict mode violation when multiple h1 elements exist
    # Keep this generic so it works across roles.
    WELCOME_MESSAGE_H1 = "h1"
    
    # Top-right account menu path (headlessui menu trigger in current UI)
    ACCOUNT_MENU_BUTTON = "header button[aria-haspopup='menu']"
    LOGOUT_MENU_ITEM = "[role='menuitem']:has-text('Log out'), button:has-text('Log out')"

    # Sidebar shortcut path (bottom icon-only logout button)
    SIDEBAR_LOGOUT_ICON = "aside div.border-t button[type='button']"
