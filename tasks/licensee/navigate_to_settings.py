from abilities.browse_the_web import BrowseTheWeb


class NavigateToSettings:
    def perform_as(self, actor):
        # Use the actor's browser to navigate the UI.
        page = actor.uses_ability(BrowseTheWeb).page

        # Open the user account menu (top right corner).
        page.click('circle[fill="#2791B5"]')  # 👈 Update selector based on your UI

        # Choose Settings from the dropdown.
        page.click("text=Settings") #Settings

        # Confirm navigation by waiting for the settings header.
        page.wait_for_selector("text=Profile Settings", timeout=10000)   #Profile Settings
