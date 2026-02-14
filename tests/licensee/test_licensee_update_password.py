import pytest


from actors import Licensee
from abilities.browse_the_web import BrowseTheWeb
from tasks.login import Login
from tasks.licensee.navigate_to_settings import NavigateToSettings
from tasks.licensee.update_profile import UpdateUserProfile
from questions.licensee.password_update_failed import PasswordUpdateFailed
from tasks.login_as import LoginAs
from config.credentials import LOGIN_CREDENTIALS

@pytest.mark.licensee
def test_MCD_LCSE_password_update_and_revert(the_licensee):
    actor = the_licensee
    
    # Use configured passwords to avoid hardcoding in the test.
    creds = LOGIN_CREDENTIALS["licensee"]
    current_password = creds["current_password"]
    new_password = creds["new_password"]
    
    # Update the password should fail in this environment.
    with pytest.raises(AssertionError, match="Incorrect current password"):
        actor.attempts_to(
            LoginAs("licensee"),
            NavigateToSettings(),
            UpdateUserProfile(new_password=new_password),
        )

    # Verify the error message is shown.
    assert the_licensee.asks_for(PasswordUpdateFailed())
