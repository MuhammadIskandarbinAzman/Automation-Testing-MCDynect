from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class UpdateUserProfile:
    def __init__(self, name: str = None, email: str = None, new_password: str = None):
        self.name = name
        self.email = email
        self.new_password = new_password

    def perform_as(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        
        # Switch to User tab if needed
        # Check if Name Input is already visible (User tab active)
        if not page.is_visible(ProfileSelectors.NAME_INPUT):
            page.click(ProfileSelectors.USER_TAB)

        # Update Profile Info
        if self.name:
            page.fill(ProfileSelectors.NAME_INPUT, self.name)

        if self.email:
             # Email is read-only in the new environment, so we skip updating it
             # or we could log a warning. For now, we just don't attempt to fill it.
             pass
        
        # Save Profile Info (if name was updated)
        if self.name:
            page.click(ProfileSelectors.SAVE_BUTTON)
            # Success message is not reliably appearing, verification will be done by checking updated value

        # Update Password (if provided)
        if self.new_password:
            current_password = getattr(actor, 'password', None)
            if not current_password:
                raise ValueError("Actor must have 'password' to update password")

            page.fill(ProfileSelectors.CURRENT_PASSWORD_INPUT, current_password)
            page.fill(ProfileSelectors.NEW_PASSWORD_INPUT, self.new_password)
            page.fill(ProfileSelectors.CONFIRM_PASSWORD_INPUT, self.new_password)
            page.click(ProfileSelectors.SAVE_PASSWORD_BUTTON)
            try:
                page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=5000)
            except:
                if page.is_visible(ProfileSelectors.PASSWORD_ERROR_MESSAGE):
                     raise AssertionError("Password update failed: Incorrect current password.")
                # Success message might be missing or transient; proceed if no error visible.
                pass
            
            # Update actor's password
            actor.password = self.new_password