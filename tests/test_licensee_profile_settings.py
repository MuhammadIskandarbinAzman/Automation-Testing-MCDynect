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
    # 1. Log in and navigate FIRST
    the_licensee.attempts_to(
        LoginAs("licensee"),
        NavigateToSettings()
    )
    
    # 2. NOW it's safe to read current profile
    original_profile = the_licensee.asks_for(GetProfileInfo())
    
    try:
        # 3. Update profile
        the_licensee.attempts_to(
            UpdateUserProfile(name="Testing 1", email="licensee@gmail.com.com")
        )
        assert the_licensee.asks_for(ProfileUpdateSuccess())
        
    finally:
        # 4. Restore ONLY if needed
        the_licensee.attempts_to(
            UpdateUserProfile(
                name=original_profile["name"],      # ⚠️ Use correct keys!
                email=original_profile["email"]
            )
        )
        assert the_licensee.asks_for(ProfileUpdateSuccess())
