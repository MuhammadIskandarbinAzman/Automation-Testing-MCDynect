"""
This module defines UI locators for the Login Page.
It centralizes how elements are found, making tests resilient to UI changes.
"""


class LoginPageUI:
    """
    Locators for elements on the login page.
    """

    # Email input field selector.
    EMAIL_FIELD = "input#email, input[id='email'], input[placeholder='me@example.com']"
    # Password input field selector.
    PASSWORD_FIELD = "input#password, input[type='password']"
    # Sign in button selector using text for stability across UI variants.
    SIGN_IN_BUTTON = "button:has-text('Sign in'), button:has-text('Login')"
    # Error message selector (supports multiple variants)
    ERROR_MESSAGE = "text=/These credentials do not match our records.|Invalid credentials/"


# --- How to create a new UI Page Locator file ---
# 1. Create a new file in this directory (e.g., `dashboard_page_ui.py`).
# 2. Define a class for the page (e.g., `DashboardPageUI`).
# 3. Add `CLASS_VARIABLES` for each element, defining their Playwright locators.
#    Example: `DASHBOARD_TITLE = "h1.dashboard-title"`.
#    Example: `USER_PROFILE_LINK = "a[aria-label='User Profile']"`.
# 4. Remember to use robust locators (role, text, CSS, XPath) and make them as specific as needed.
