import pytest


from actors import Licensee
from abilities.browse_the_web import BrowseTheWeb
from tasks.login import Login
from tasks.licensee.navigate_to_settings import NavigateToSettings
from tasks.licensee.update_profile import UpdateUserProfile
from questions.licensee.profile_saved import ProfileUpdateSuccess
from tasks.login_as import LoginAs
from config.credentials import LOGIN_CREDENTIALS

@pytest.mark.licensee
def test_MCD_LCSE_password_update_and_revert(the_licensee):
    actor = the_licensee
    
    # Use configured passwords to avoid hardcoding in the test.
    creds = LOGIN_CREDENTIALS["licensee"]
    current_password = creds["current_password"]
    new_password = creds["new_password"]
    
    try:
        # Update the password to the new value.
        actor.attempts_to(
            LoginAs("licensee"),
            NavigateToSettings(),
            UpdateUserProfile(new_password=new_password)
        )

        # Verify success.
        assert the_licensee.asks_for(ProfileUpdateSuccess())

        # Keep actor password in sync for subsequent actions.
        actor.password = new_password
    finally:
        # Revert password so other tests can run in the same suite.
        actor.attempts_to(
            LoginAs("licensee"),
            NavigateToSettings(),
            UpdateUserProfile(new_password=current_password)
        )
        # Verify the revert succeeded and reset the actor state.
        assert the_licensee.asks_for(ProfileUpdateSuccess())
        actor.password = current_password
