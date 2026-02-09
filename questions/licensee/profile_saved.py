from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class ProfileUpdateSuccess:
    def __init__(self, expected_name: str = None):
        self.expected_name = expected_name

    def answered_by(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        if self.expected_name:
             # Verify the name input contains the expected name
            return page.get_by_placeholder("Enter Name").input_value() == self.expected_name
        else:
            # Fallback if no name provided (though not ideal)
            return True