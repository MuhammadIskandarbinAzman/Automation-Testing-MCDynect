# questions/licensee/get_profile_info.py
from abilities.browse_the_web import BrowseTheWeb
from ..questions import Question
from config.selectors import ProfileSelectors

class GetProfileInfo(Question):
    def answered_by(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        page.click(ProfileSelectors.USER_TAB)
        
        # Wait for fields to be ready
        page.wait_for_selector("#name", state="visible", timeout=5000)
        page.wait_for_selector("#email", state="visible", timeout=5000)
        
        return {
            "name": page.input_value("#name"),
            "email": page.input_value("#email")
        }