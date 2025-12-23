"""
This module defines the Login task.
Tasks represent high-level business actions an Actor attempts.
"""
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.login_page_ui import LoginPageUI

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
        browser.go_to("https://staging.mrchurros.com.my/login") # Consider making this dynamic from config
        browser.find_and_fill(LoginPageUI.EMAIL_FIELD, self.email)
        browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, self.password)
        browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)

# --- How to create a new Task ---
# 1. Create a new file in this directory (e.g., `add_product_to_cart.py`).
# 2. Define a class (e.g., `AddProductToCart`).
# 3. Implement an `__init__` method to accept any necessary parameters (e.g., `product_name`, `quantity`).
# 4. Implement a `@staticmethod` factory method (e.g., `AddProductToCart.named(product_name, quantity)`).
# 5. Implement the `perform_as(self, actor: Actor)` method:
#    - Get necessary abilities: `browser = actor.uses_ability(BrowseTheWeb)`.
#    - Use the ability methods and UI locators to define the steps of the task.
#      Example: `browser.find_and_click(ProductPageUI.ADD_TO_CART_BUTTON(self.product_name))`.

