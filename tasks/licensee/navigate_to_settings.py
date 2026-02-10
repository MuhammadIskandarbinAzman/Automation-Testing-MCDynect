from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL


class NavigateToSettings:
    def perform_as(self, actor):
        # Use the actor's browser to navigate the UI.
        page = actor.uses_ability(BrowseTheWeb).page

        try:
            # Click User Account Menu Icon (sidebar menu button)
            menu_btn = page.locator(
                'button[data-sidebar="menu-button"][data-slot="dropdown-menu-trigger"]'
            )
            menu_btn.wait_for(state="visible", timeout=15000)
            menu_btn.click(force=True)

            # Click 'Account Settings' from dropdown
            settings_option = page.locator("text=Account Settings")
            settings_option.wait_for(state="visible", timeout=5000)
            settings_option.click(force=True)

            page.wait_for_url("**/settings", timeout=10000)
        except Exception:
            # Fallback: older UI or direct navigation
            try:
                page.click('circle[fill="#2791B5"]')
                page.click("text=Settings")
            except Exception:
                page.goto(f"{BASE_URL}/settings")

            page.wait_for_url("**/settings", timeout=10000)

        page.locator("text=Profile Settings").first.wait_for(timeout=15000)
