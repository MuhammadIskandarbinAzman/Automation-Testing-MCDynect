from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from ui.dashboard_page_ui import DashboardPageUI


class Logout:
    def __init__(self, use_sidebar: bool = False):
        self.use_sidebar = use_sidebar

    @staticmethod
    def from_user_menu():
        return Logout(use_sidebar=False)

    @staticmethod
    def from_sidebar():
        return Logout(use_sidebar=True)

    def perform_as(self, actor: Actor):
        browser = actor.uses_ability(BrowseTheWeb)
        page = browser.page

        def click_first_visible(selectors):
            for selector in selectors:
                locator = page.locator(selector)
                if locator.count() > 0 and locator.first.is_visible():
                    locator.first.click()
                    return True
            return False

        if self.use_sidebar:
            clicked = click_first_visible(
                [
                    DashboardPageUI.SIDEBAR_LOGOUT_ICON,
                    "aside [role='menuitem']:has-text('Log out')",
                    "aside button:has-text('Log out')",
                    "aside a:has-text('Log out')",
                ]
            )
            if not clicked:
                raise AssertionError("Sidebar logout button was not found.")
        else:
            menu_clicked = click_first_visible([DashboardPageUI.ACCOUNT_MENU_BUTTON])
            if not menu_clicked:
                raise AssertionError("Account menu button was not found.")

            clicked = click_first_visible(
                [
                    DashboardPageUI.LOGOUT_MENU_ITEM,
                    "[role='menuitem']:has-text('Logout')",
                    "button:has-text('Logout')",
                ]
            )
            if not clicked:
                raise AssertionError("Logout menu item was not found.")

        page.wait_for_url("**/login", timeout=15000)
