class ProfileSelectors:
    # Tabs
    USER_TAB = "text=User"
    COMPANY_TAB = "text=Company"

    # Profile Information Section - FROM CODEGEN
    NAME_INPUT = "#Name"      # ← From: page.get_by_role("textbox", name="Name")
    EMAIL_INPUT = "#Email"    # ← From: page.get_by_role("textbox", name="Email")
    SAVE_BUTTON = 'form:has-text("NameEmailSave") >> button'  # ← From codegen

    # Password Section (keep existing)
    CURRENT_PASSWORD_INPUT = 'textbox[name="Current Password"]'
    NEW_PASSWORD_INPUT = 'textbox[name="New Password"]'
    CONFIRM_PASSWORD_INPUT = 'textbox[name="Confirm New Password"]'
    #SAVE_PASSWORD_BUTTON = 'form:has-text("Current PasswordNew PasswordConfirm New PasswordSave") >> button'

    SUCCESS_MESSAGE = "text=Saved"
    PASSWORD_ERROR_MESSAGE = "text=The password is incorrect."