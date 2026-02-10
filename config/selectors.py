class ProfileSelectors:
    # Tabs
    USER_TAB = 'button:has-text("User")'
    COMPANY_TAB = "text=Company"

    # Profile Information Section (support multiple environments)
    NAME_INPUT = "#Name, #name, input[placeholder='Enter Name']"
    EMAIL_INPUT = "#Email, #email, input[readonly], input[disabled]"

    # Save buttons (profile vs password)
    PROFILE_SAVE_BUTTON = (
        'form:has-text("Name") button:has-text("Save"), '
        'form:has-text("Email") button:has-text("Save"), '
        'button:has-text("Save")'
    )
    PASSWORD_SAVE_BUTTON = (
        'div:has-text("Update Password") button:has-text("Save"), '
        'form:has-text("Password") button:has-text("Save"), '
        'button:has-text("Save")'
    )

    # Password Section
    CURRENT_PASSWORD_INPUT = "#current_password, input[placeholder='Enter Old Password']"
    NEW_PASSWORD_INPUT = "#password, input[placeholder='Enter New Password']"
    CONFIRM_PASSWORD_INPUT = "#password_confirmation, input[placeholder='Enter Confirm Password']"

    # Backwards-compatible aliases
    SAVE_BUTTON = PROFILE_SAVE_BUTTON
    SAVE_PASSWORD_BUTTON = PASSWORD_SAVE_BUTTON

    # Generic success and error indicators used by questions.
    SUCCESS_MESSAGE = "text=Saved"
    PASSWORD_ERROR_MESSAGE = "text=The password is incorrect."
