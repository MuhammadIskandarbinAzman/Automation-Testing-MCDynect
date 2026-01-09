from abilities.browse_the_web import BrowseTheWeb


class NavigateToSettings:
    def perform_as(self, actor):
        page = actor.uses_ability(BrowseTheWeb).page

        # Click User Account Menu Icon (top right corner)
        page.click('circle[fill="#2791B5"]')  # 👈 Update selector based on your UI

        # Click 'Settings' from dropdown
        page.click("text=Settings") #Settings

        # Wait for Profile Settings Page
        page.wait_for_selector("text=Profile Settings", timeout=10000)   #Profile Settings