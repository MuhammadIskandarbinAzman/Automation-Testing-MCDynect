from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors


class ProfileUpdateSuccess:
    def __init__(self, expected_name: str = None):
        self.expected_name = expected_name

    def answered_by(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        if self.expected_name:
            # Verify the name input contains the expected name
            return page.input_value(ProfileSelectors.NAME_INPUT) == self.expected_name

        # Fallback to generic success toast/message after save.
        return page.is_visible(ProfileSelectors.SUCCESS_MESSAGE)
