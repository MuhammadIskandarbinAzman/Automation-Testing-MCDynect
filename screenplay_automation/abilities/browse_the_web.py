from playwright.sync_api import Page

class BrowseTheWeb:
    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def with_browser_page(page: Page) -> "BrowseTheWeb":
        return BrowseTheWeb(page)

    def go_to(self, url: str) -> None:
        self.page.goto(url)

    def find_and_fill(self, locator: str, value: str) -> None:
        self.page.locator(locator).fill(value)

    def find_and_click(self, locator: str) -> None:
        self.page.locator(locator).click()

    def find_text_content(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    def find_and_check_visibility(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

    def check_url(self) -> str:
        return self.page.url

