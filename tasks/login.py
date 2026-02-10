"""
This module defines the Login task.
Tasks represent high-level business actions an Actor attempts.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.login_page_ui import LoginPageUI
from ui.onboarding_page_ui import OnboardingPageUI
from config.credentials import BASE_URL
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class Login:
    """
    A task for an Actor to log into the application.
    """

    def __init__(self, email, password):
        # Store credentials for this login attempt.
        self.email = email
        self.password = password

    @staticmethod
    def with_credentials(email, password):
        """
        Factory method to create a Login task with specific credentials.
        Example: `Login.with_credentials("user@example.com", "password")`
        """
        # Factory to keep call sites concise.
        return Login(email, password)

    def perform_as(self, actor: Actor):
        """
        Performs the login action using the Actor's BrowseTheWeb ability.
        """
        # Use the actor's browser ability to drive the UI.
        browser = actor.uses_ability(BrowseTheWeb)
        # Ensure we are logged out before attempting a new login.
        browser.clear_session()
        # Navigate to login page using configurable base URL.
        browser.go_to(f"{BASE_URL}/login")

        page = browser.page
        try:
            page.wait_for_selector(LoginPageUI.EMAIL_FIELD, timeout=5000)
        except PlaywrightTimeoutError:
            # Only skip if we were redirected off the login route.
            if "/login" in page.url:
                raise
            return

        # Fill credentials and submit the form.
        browser.find_and_fill(LoginPageUI.EMAIL_FIELD, self.email)
        browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, self.password)
        browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)

        # After sign in, wait a moment for the page to start loading
        page.wait_for_timeout(2000)

        # We may be redirected to the onboarding page
        try:
            if page.is_visible(OnboardingPageUI.ONBOARDING_HEADER):
                # Infer role label from actor class (e.g., AreaManager -> "Area Manager").
                role_label = "".join(
                    [
                        (" " + ch if ch.isupper() and i > 0 else ch)
                        for i, ch in enumerate(actor.__class__.__name__)
                    ]
                ).strip()
                open_role = page.locator(f"text=Open {role_label}")
                if open_role.count() > 0:
                    open_role.first.click()
                else:
                    page.locator(OnboardingPageUI.OPEN_MODULE_BUTTON).first.click()
                page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"Onboarding button not found or timed out: {str(e)}")
            pass


# --- How to create a new Task ---
# 1. Create a new file in this directory (e.g., `add_product_to_cart.py`).
# 2. Define a class (e.g., `AddProductToCart`).
# 3. Implement an `__init__` method to accept any necessary parameters (e.g., `product_name`, `quantity`).
# 4. Implement a `@staticmethod` factory method (e.g., `AddProductToCart.named(product_name, quantity)`).
# 5. Implement the `perform_as(self, actor: Actor)` method:
#    - Get necessary abilities: `browser = actor.uses_ability(BrowseTheWeb)`.
#    - Use the ability methods and UI locators to define the steps of the task.
#      Example: `browser.find_and_click(ProductPageUI.ADD_TO_CART_BUTTON(self.product_name))`.
