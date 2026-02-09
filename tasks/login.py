"""
This module defines the Login task.
Tasks represent high-level business actions an Actor attempts.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.login_page_ui import LoginPageUI
from ui.onboarding_page_ui import OnboardingPageUI
from config.credentials import BASE_URL

class Login:
    """
    A task for an Actor to log into the application.
    """
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def with_credentials(email, password):
        """
        Factory method to create a Login task with specific credentials.
        Example: `Login.with_credentials("user@example.com", "password")`
        """
        return Login(email, password)

    def perform_as(self, actor: Actor):
        """
        Performs the login action using the Actor's BrowseTheWeb ability.
        """
        browser = actor.uses_ability(BrowseTheWeb)
        browser.go_to(f"{BASE_URL}/login")
        browser.find_and_fill(LoginPageUI.EMAIL_FIELD, self.email)
        browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, self.password)
        browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)
        
        # After sign in, wait a moment for the page to start loading
        browser.page.wait_for_timeout(2000)
        
        # We are redirected to the on-boarding page (/)
        # Wait for the on-boarding button to appear
        try:
            # Wait for the on-boarding button to be visible
            button = browser.page.locator(OnboardingPageUI.OPEN_MODULE_BUTTON)
            button.wait_for(state="visible", timeout=15000)
            browser.find_and_click(OnboardingPageUI.OPEN_MODULE_BUTTON)
            # Wait for navigation to dashboard after clicking
            browser.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            # If it's not visible, we might have skipped it or landed elsewhere.
            # We'll let the following assertions in the test handle failure.
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

