from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
import pytest

def test_successful_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    login_page.login("licensee@gmail.com", "masterpassword1234")  # Replace with valid credentials if available
    # Add assertions for successful login, e.g., check for a welcome message or URL change
    # For now, let's assume a successful login redirects to a dashboard or main page
    assert page.url != "https://staging.mrchurros.com.my/licensee/dashboard", "Login failed: URL did not change"
    assert login_page.welcome_back_message.is_visible(), "'Welcome Back' message not displayed after successful login"

def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    login_page.login("invalid_user", "invalid_password")
    # Assert that an error message is displayed
    expect(login_page.error_message).to_contain_text("These credentials do not match our records.")

