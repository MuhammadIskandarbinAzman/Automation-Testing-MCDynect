"""
This module defines UI locators for the Login Page.
It centralizes how elements are found, making tests resilient to UI changes.
"""
class LoginPageUI:
    """
    Locators for elements on the login page.
    """
    EMAIL_FIELD = "input[placeholder='me@example.com']"
    PASSWORD_FIELD = "input[type='password']"
    SIGN_IN_BUTTON = "role=button[name='Login']"
    # Error message for invalid credentials (displayed as a toast notification)
    # Using a more flexible locator that matches any element containing this text
    ERROR_MESSAGE = "text=Invalid credentials"

# --- How to create a new UI Page Locator file ---
# 1. Create a new file in this directory (e.g., `dashboard_page_ui.py`).
# 2. Define a class for the page (e.g., `DashboardPageUI`).
# 3. Add `CLASS_VARIABLES` for each element, defining their Playwright locators.
#    Example: `DASHBOARD_TITLE = "h1.dashboard-title"`.
#    Example: `USER_PROFILE_LINK = "a[aria-label='User Profile']"`.
# 4. Remember to use robust locators (role, text, CSS, XPath) and make them as specific as needed.

