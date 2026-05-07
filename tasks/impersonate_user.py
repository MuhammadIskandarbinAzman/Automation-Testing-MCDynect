"""
Task for admin impersonation.
"""
import re
from urllib.parse import quote_plus

from actors.base_actor import Actor
from abilities.browse_the_web import BrowseTheWeb
from config.credentials import BASE_URL
from ui.admin_impersonation_page_ui import AdminImpersonationPageUI


class ImpersonateUser:
    """
    Allows an admin actor to impersonate the first user matching a search term.
    """

    def __init__(self, search_term: str):
        self.search_term = search_term

    @staticmethod
    def matching(search_term: str) -> "ImpersonateUser":
        return ImpersonateUser(search_term)

    def perform_as(self, actor: Actor) -> None:
        browser = actor.uses_ability(BrowseTheWeb)
        page = browser.page

        browser.go_to(f"{BASE_URL}/admin/dashboard")
        page.get_by_role(
            "link",
            name=AdminImpersonationPageUI.IMPERSONATE_LINK_TEXT,
        ).click()

        search_input = page.locator(AdminImpersonationPageUI.SEARCH_INPUT).first
        search_input.wait_for(state="visible", timeout=10000)
        search_input.fill(self.search_term)

        # Navigate directly to the filtered result route so the flow is stable
        # even if search debounce timing changes.
        browser.go_to(
            f"{BASE_URL}/admin/impersonate?search={quote_plus(self.search_term)}"
        )

        matching_row = page.get_by_role(
            "row",
            name=re.compile(re.escape(self.search_term), re.IGNORECASE),
        ).first
        matching_row.wait_for(state="visible", timeout=10000)
        matching_row.get_by_role("button").first.click()

        page.wait_for_load_state("domcontentloaded", timeout=10000)
        maybe_later = page.locator(AdminImpersonationPageUI.MAYBE_LATER_BUTTON)
        try:
            maybe_later.first.wait_for(state="visible", timeout=3000)
            maybe_later.first.click()
        except Exception:
            pass
