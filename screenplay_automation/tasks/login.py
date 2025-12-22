from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.login_page_ui import LoginPageUI

class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def with_credentials(email, password):
        return Login(email, password)

    def perform_as(self, actor: Actor):
        browser = actor.uses_ability(BrowseTheWeb)
        browser.go_to("https://staging.mrchurros.com.my/login")
        browser.find_and_fill(LoginPageUI.EMAIL_FIELD, self.email)
        browser.find_and_fill(LoginPageUI.PASSWORD_FIELD, self.password)
        browser.find_and_click(LoginPageUI.SIGN_IN_BUTTON)

