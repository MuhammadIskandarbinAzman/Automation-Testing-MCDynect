from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class UpdateUserProfile:
    def __init__(self, name: str = None, email: str = None, new_password: str = None):
        self.name = name
        self.email = email
        self.new_password = new_password

    def perform_as(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        
        # Switch to User tab
        page.click(ProfileSelectors.USER_TAB)

        # Update Profile Info
        if self.name:
            page.get_by_role("textbox", name="Name").fill(self.name)  # ✅ Removed .click()

        if self.email:
            page.get_by_role("textbox", name="Email").fill(self.email)  # ✅ Removed .click()
        
        # Save Profile Info (if either field was updated)
        if self.name or self.email:
            page.click(ProfileSelectors.SAVE_BUTTON)
            page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=10000)

        # Update Password (if provided)
        if self.new_password:
            current_password = getattr(actor, 'password', None)
            if not current_password:
                raise ValueError("Actor must have 'password' to update password")

            page.fill(ProfileSelectors.CURRENT_PASSWORD_INPUT, current_password)
            page.fill(ProfileSelectors.NEW_PASSWORD_INPUT, self.new_password)
            page.fill(ProfileSelectors.CONFIRM_PASSWORD_INPUT, self.new_password)
            page.click(ProfileSelectors.SAVE_PASSWORD_BUTTON)
            page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=10000)
            
            # Update actor's password
            actor.password = self.new_password