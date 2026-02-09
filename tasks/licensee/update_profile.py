import time

from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors

class UpdateUserProfile:
    def __init__(self, name: str = None, email: str = None, new_password: str = None):
        # Optional fields allow reusing this task for profile and password updates.
        self.name = name
        self.email = email
        self.new_password = new_password

    def perform_as(self, actor):
        # Use the actor's browser page for direct Playwright actions.
        page = actor.uses_ability(BrowseTheWeb).page
        
        # Ensure we are on the User profile tab before editing.
        page.click(ProfileSelectors.USER_TAB)

        # Update profile fields if provided.
        if self.name:
            page.get_by_role("textbox", name="Name").fill(self.name)  # ✅ Removed .click()

        if self.email:
            page.get_by_role("textbox", name="Email").fill(self.email)  # ✅ Removed .click()
        
        # Save profile changes only when at least one field changed.
        if self.name or self.email:
            page.click(ProfileSelectors.PROFILE_SAVE_BUTTON)
            page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=10000)

        # Update password only when a new password is provided.
        if self.new_password:
            # Current password must be stored on the actor (from credentials).
            current_password = getattr(actor, 'password', None)
            if not current_password:
                raise ValueError("Actor must have 'password' to update password")

            page.fill(ProfileSelectors.CURRENT_PASSWORD_INPUT, current_password)
            print("Filled CURRENT_PASSWORD_INPUT:", current_password)
            page.screenshot(path="step1_current_password_filled.png")
            time.sleep(1)

            page.fill(ProfileSelectors.NEW_PASSWORD_INPUT, self.new_password)
            print("Filled NEW_PASSWORD_INPUT:", self.new_password)
            page.screenshot(path="step2_new_password_filled.png")
            time.sleep(1)

            page.fill(ProfileSelectors.CONFIRM_PASSWORD_INPUT, self.new_password)
            print("Filled CONFIRM_PASSWORD_INPUT:", self.new_password)
            page.screenshot(path="step3_confirm_password_filled.png")
            time.sleep(1)

            # Submit password change and wait for the success toast.
            page.click(ProfileSelectors.PASSWORD_SAVE_BUTTON)
            page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=10000)
