class ProfileSelectors:
    # Tabs
    USER_TAB = "text=User"
    COMPANY_TAB = "text=Company"

    # Profile Information Section - FROM CODEGEN
    NAME_INPUT = "#Name"      # ← From: page.get_by_role("textbox", name="Name")
    EMAIL_INPUT = "#Email"    # ← From: page.get_by_role("textbox", name="Email")
    PROFILE_SAVE_BUTTON = 'form:has-text("NameEmailSave") >> button'  # ← From codegen

    # Password Section (keep existing)
    CURRENT_PASSWORD_INPUT = '#current_password'
    NEW_PASSWORD_INPUT = '#password'
    CONFIRM_PASSWORD_INPUT = '#password_confirmation'
    PASSWORD_SAVE_BUTTON = 'button:has-text("Save")'

    # Backwards-compatible alias (prefer PROFILE_SAVE_BUTTON / PASSWORD_SAVE_BUTTON)
    SAVE_BUTTON = PROFILE_SAVE_BUTTON

    # Generic success and error indicators used by questions.
    SUCCESS_MESSAGE = "text=Saved"
    PASSWORD_ERROR_MESSAGE = "text=The password is incorrect."
