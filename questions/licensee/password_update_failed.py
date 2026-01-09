from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class PasswordUpdateFailed:
    @staticmethod
    def answered_by(actor):
        page = actor.uses_ability_to(BrowseTheWeb).page
        return page.is_visible(ProfileSelectors.PASSWORD_ERROR_MESSAGE)