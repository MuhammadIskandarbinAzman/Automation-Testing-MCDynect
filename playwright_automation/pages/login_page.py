from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.locator("//input[@id='email']")
        self.password_field = self.page.locator("//input[@id='password']")
        self.login_button = self.page.get_by_role("button", name="Sign in")
        self.error_message = self.page.locator("p.text-error-500").first
        self.welcome_back_message = self.page.locator("text=Welcome Back")

    def navigate_to_login_page(self):
        self.navigate("https://staging.mrchurros.com.my/login")

    def login(self, email, password):
        self.username_field.fill(email)
        self.password_field.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.text_content()

