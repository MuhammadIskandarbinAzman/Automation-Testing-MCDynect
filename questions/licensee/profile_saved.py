from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class ProfileUpdateSuccess:
    @staticmethod
    def answered_by(actor):
        page = actor.uses_ability(BrowseTheWeb).page
        return page.is_visible(ProfileSelectors.SUCCESS_MESSAGE)