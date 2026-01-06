# screenplay_automation/questions/current_url.py
from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb

class CurrentURL:
    @staticmethod
    def value_for(actor: Actor) -> str:
        browser = actor.uses_ability(BrowseTheWeb)
        return browser.check_url()