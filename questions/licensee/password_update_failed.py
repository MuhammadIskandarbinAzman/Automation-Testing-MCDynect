from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class PasswordUpdateFailed:
    @staticmethod
    def answered_by(actor):
        # Check for the specific password error message.
        page = actor.uses_ability(BrowseTheWeb).page
        return page.is_visible(ProfileSelectors.PASSWORD_ERROR_MESSAGE)
