"""
This module defines UI locators for the On-boarding Page.
"""
class OnboardingPageUI:
    """
    Locators for elements on the on-boarding page.
    """
    # The "Open [Module]" button/link that leads to the dashboard
    # Works for "Open Licensee", "Open Area Manager", etc.
    # Text selector is safest here; we'll pick the first match in the task.
    OPEN_MODULE_BUTTON = "text=Open"
    
    # Header to verify we are on the on-boarding page
    ONBOARDING_HEADER = "h1:has-text('Welcome to Your On Boarding')"
