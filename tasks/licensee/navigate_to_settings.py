from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL
from config.selectors import ProfileSelectors


class NavigateToSettings:
    def perform_as(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page
        current_url = page.url

        try:
            # If profile page is already open and form controls exist, no work needed.
            if "/licensee/profile" in current_url and (
                page.locator(ProfileSelectors.NAME_INPUT).count() > 0
                or page.locator(ProfileSelectors.USER_TAB).count() > 0
            ):
                return

            # Open top-right account menu and click Settings.
            menu_btn = page.locator("header button[aria-haspopup='menu']").first
            menu_btn.wait_for(state="visible", timeout=10000)
            menu_btn.click()

            settings_option = page.locator("[role='menuitem']:has-text('Settings'), button:has-text('Settings')").first
            settings_option.wait_for(state="visible", timeout=5000)
            settings_option.click()
            page.wait_for_url("**/licensee/profile", timeout=15000)
        except Exception:
            # Fallback to known profile URL for the licensee role.
            page.goto(f"{BASE_URL}/licensee/profile")

        page.wait_for_load_state("domcontentloaded", timeout=10000)
        if "/licensee/profile" not in page.url:
            raise AssertionError(f"Failed to navigate to licensee profile page. Current URL: {page.url}")
