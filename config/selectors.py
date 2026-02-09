class ProfileSelectors:
    # Tabs
    USER_TAB = 'button:has-text("User")'
    COMPANY_TAB = "text=Company"

    # Profile Information Section
    NAME_INPUT = "input[placeholder='Enter Name']"
    EMAIL_INPUT = "input[readonly], input[disabled]" # Email is read-only in this environment
    SAVE_BUTTON = 'button:has-text("Save")'

    # Password Section
    CURRENT_PASSWORD_INPUT = "input[placeholder='Enter Old Password']"
    NEW_PASSWORD_INPUT = "input[placeholder='Enter New Password']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder='Enter Confirm Password']"
    # The screenshot shows a secondary "Save" button in the password section.
    # Assuming it's the second button of type 'submit' or similar, or we can scope it.
    # A safer bet based on likely structure is scoping to the password container if possible,
    # but since we don't have the HTML, let's try a more specific text match or order if uniqueness is an issue.
    # However, 'button:has-text("Save")' appears twice.
    # Let's use the layout to differentiate or use :nth-match if needed.
    # Based on the screenshot, there are two distinct cards.
    # Let's try to target the Save button specifically for the password section.
    SAVE_PASSWORD_BUTTON = 'div:has-text("Update Password") >> button:has-text("Save")'

    SUCCESS_MESSAGE = "text=Saved"
    PASSWORD_ERROR_MESSAGE = "text=The password is incorrect."