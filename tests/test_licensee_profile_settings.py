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
from config.credentials import LOGIN_CREDENTIALS

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
            UpdateUserProfile(name="Testing 1")
        )
        assert the_licensee.asks_for(ProfileUpdateSuccess(expected_name="Testing 1"))
        
    finally:
        # 4. Restore ONLY if needed
        the_licensee.attempts_to(
            UpdateUserProfile(
                name=original_profile["name"]
            )
        )
        assert the_licensee.asks_for(ProfileUpdateSuccess(expected_name=original_profile["name"]))

@pytest.mark.licensee
def test_MCD_LCSE_03_update_password_success(the_licensee):
    # 1. Setup actor with initial password
    initial_password = LOGIN_CREDENTIALS["licensee"]["password"]
    the_licensee.password = initial_password
    new_password = "newPassword123!"
    
    # 2. Log in and navigate
    the_licensee.attempts_to(
        LoginAs("licensee"),
        NavigateToSettings()
    )
    
    # 3. VERIFY we're on the correct page BEFORE update
    from abilities.browse_the_web import BrowseTheWeb
    
    page = the_licensee.ability_to(BrowseTheWeb).page
    current_url = page.url
    print(f"DEBUG: Current URL after navigation = {current_url}")
    
    # Check if we're on an error page or redirected to login
    if "404" in current_url or "not-found" in current_url.lower():
        pytest.fail(f"Got 404 error. URL: {current_url}")
    
    if "login" in current_url.lower() or "signin" in current_url.lower():
        pytest.fail(f"Redirected to login page. URL: {current_url}")
    
    try:
        # 4. Update password
        the_licensee.attempts_to(
            UpdateUserProfile(new_password=new_password)
        )
        
        # 5. Verify success
        assert the_licensee.password == new_password, "Password not updated in actor"
        
    except Exception as e:
        print(f"⚠️ Password update failed: {e}")
        raise
    finally:
        # 6. Restore original password
        if the_licensee.password != initial_password:
            try:
                the_licensee.attempts_to(
                    UpdateUserProfile(new_password=initial_password)
                )
                the_licensee.password = initial_password
                print("✅ Password restored successfully")
            except Exception as cleanup_error:
                print(f"⚠️ Cleanup warning: {cleanup_error}")
                # Don't re-raise - let primary test error be reported
