from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb

class WelcomeMessage:
    @staticmethod
    def is_visible_to(actor: Actor) -> bool:
        browser = actor.uses_ability(BrowseTheWeb)
        return browser.find_and_check_visibility("text=Welcome Back")

    @staticmethod
    def text_for(actor: Actor) -> str:
        browser = actor.uses_ability(BrowseTheWeb)
        return browser.find_text_content("text=Welcome Back")

