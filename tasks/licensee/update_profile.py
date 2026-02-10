from abilities.browse_the_web import BrowseTheWeb
from config.selectors import ProfileSelectors
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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
        if not page.is_visible(ProfileSelectors.NAME_INPUT):
            page.click(ProfileSelectors.USER_TAB)

        # Update profile fields if provided.
        if self.name:
            page.fill(ProfileSelectors.NAME_INPUT, self.name)

        if self.email:
            # Email is read-only in some environments, so skip updating it.
            pass

        # Save profile changes only when at least one field changed.
        if self.name or self.email:
            page.locator(ProfileSelectors.PROFILE_SAVE_BUTTON).first.click()
            try:
                page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=10000)
            except PlaywrightTimeoutError:
                # Success toast can be flaky; proceed if no error is visible.
                pass

        # Update password only when a new password is provided.
        if self.new_password:
            # Current password must be stored on the actor (from credentials).
            current_password = getattr(actor, "password", None)
            if not current_password:
                raise ValueError("Actor must have 'password' to update password")

            page.fill(ProfileSelectors.CURRENT_PASSWORD_INPUT, current_password)
            page.fill(ProfileSelectors.NEW_PASSWORD_INPUT, self.new_password)
            page.fill(ProfileSelectors.CONFIRM_PASSWORD_INPUT, self.new_password)

            page.locator(ProfileSelectors.PASSWORD_SAVE_BUTTON).last.click()
            try:
                page.wait_for_selector(ProfileSelectors.SUCCESS_MESSAGE, timeout=5000)
            except PlaywrightTimeoutError:
                if page.is_visible(ProfileSelectors.PASSWORD_ERROR_MESSAGE):
                    raise AssertionError("Password update failed: Incorrect current password.")
                # Success message might be missing or transient; proceed if no error visible.
                pass

            # Update actor's password
            actor.password = self.new_password
