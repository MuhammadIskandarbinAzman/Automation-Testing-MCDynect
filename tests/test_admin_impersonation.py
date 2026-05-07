import pytest

from actors.admin import Admin
from abilities.browse_the_web import BrowseTheWeb
from config.credentials import get_admin_credentials, get_impersonation_targets
from questions.current_url import CurrentURL
from tasks.impersonate_user import ImpersonateUser
from tasks.login import Login


@pytest.mark.parametrize(
    "role,target",
    get_impersonation_targets().items(),
    ids=lambda value: value if isinstance(value, str) else value["search"],
)
def test_admin_can_impersonate_user_roles(the_admin: Admin, role: str, target: dict[str, str]):
    credentials = get_admin_credentials()
    the_admin.attempts_to(
        Login.with_credentials(credentials["email"], credentials["password"]),
        ImpersonateUser.matching(target["search"]),
    )

    browser = the_admin.uses_ability(BrowseTheWeb)
    browser.page.wait_for_url(target["expected_url"], timeout=10000)
    browser.page.wait_for_load_state("networkidle", timeout=10000)

    assert CurrentURL.value_for(the_admin) == target["expected_url"], (
        f"Expected admin to impersonate {role} and land on "
        f"{target['expected_url']}, got {CurrentURL.value_for(the_admin)}"
    )
