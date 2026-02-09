# questions/licensee/get_profile_info.py
from abilities.browse_the_web import BrowseTheWeb
from ..questions import Question
from config.selectors import ProfileSelectors

class GetProfileInfo(Question):
    def answered_by(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        page.click(ProfileSelectors.USER_TAB)
        
        # Wait for fields to be ready
        page.wait_for_selector(ProfileSelectors.NAME_INPUT, state="visible", timeout=5000)
        page.wait_for_selector(ProfileSelectors.EMAIL_INPUT, state="visible", timeout=5000)
        
        return {
            "name": page.input_value(ProfileSelectors.NAME_INPUT),
            "email": page.input_value(ProfileSelectors.EMAIL_INPUT)
        }