import pytest


from actors import Licensee
from abilities.browse_the_web import BrowseTheWeb
from tasks.login import Login  # ← Changed from LoginToMCdynect to Login
from tasks.licensee.navigate_to_settings import NavigateToSettings
from tasks.licensee.update_profile import UpdateUserProfile
from questions.licensee.profile_saved import ProfileUpdateSuccess
from questions.licensee.password_update_failed import PasswordUpdateFailed
from tasks.login_as import LoginAs
from questions.licensee.get_profile_info import GetProfileInfo

@pytest.mark.licensee
def test_MCD_LCSE_02_update_profile_success(the_licensee):
    original_profile = the_licensee.asks_for(GetProfileInfo())
    
    try:
        the_licensee.attempts_to(
            LoginAs("licensee"),
            NavigateToSettings(),
            UpdateUserProfile(name="Testing 1", email="licensee@gmail.com.com")
        )
        assert the_licensee.should_see_the(ProfileUpdateSuccess())
        
    finally:
        the_licensee.attempts_to(
            NavigateToSettings(),
            UpdateUserProfile(
                name=original_profile["UAT Testing"],
                email=original_profile["licensee@gmail.com"]
            )
        )
        assert the_licensee.should_see_the(ProfileUpdateSuccess())
@pytest.mark.licensee
def test_MCD_LCSE_02_access_user_profile_failed(the_licensee):
    the_licensee.attempts_to(
        LoginAs("licensee"),  # ✅ No credentials in test
        NavigateToSettings(),
        UpdateUserProfile(name="Updated Name", email="updated@example.com")
    )
    assert the_licensee.should_see_the(PasswordUpdateFailed())