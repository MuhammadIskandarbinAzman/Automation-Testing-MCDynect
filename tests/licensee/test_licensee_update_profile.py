import pytest


from actors import Licensee
from abilities.browse_the_web import BrowseTheWeb
from tasks.login import Login
from tasks.licensee.navigate_to_settings import NavigateToSettings
from tasks.licensee.update_profile import UpdateUserProfile
from questions.licensee.profile_saved import ProfileUpdateSuccess
from tasks.login_as import LoginAs
from questions.licensee.get_profile_info import GetProfileInfo

@pytest.mark.licensee
def test_MCD_LCSE_02_update_profile_success(the_licensee):
    # 1. Log in and navigate to settings first.
    the_licensee.attempts_to(
        LoginAs("licensee"),
        NavigateToSettings()
    )
    
    # 2. Capture current profile so we can restore it later.
    original_profile = the_licensee.asks_for(GetProfileInfo())
    
    try:
        # 3. Update profile fields.
        the_licensee.attempts_to(
            UpdateUserProfile(name="Testing 1", email="licensee@gmail.com.com")
        )
        # 4. Assert the update succeeded.
        assert the_licensee.asks_for(ProfileUpdateSuccess())
        
    finally:
        # 5. Restore original profile to keep tests idempotent.
        the_licensee.attempts_to(
            UpdateUserProfile(
                name=original_profile["name"],
                email=original_profile["email"]
            )
        )
        # 6. Confirm the restore succeeded.
        assert the_licensee.asks_for(ProfileUpdateSuccess())
