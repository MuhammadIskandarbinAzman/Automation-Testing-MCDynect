"""
This module stores configuration data such as login credentials and base URLs.
Centralizing this data makes it easy to manage and adapt to different environments (e.g., staging, production).
"""
LOGIN_CREDENTIALS = {
    "licensee": {
        "email": "licensee@gmail.com",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/licensee/dashboard" # Actual URL after successful login
    },
    "area_manager": {
        "email": "aiman.ghazali@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/area-manager/dashboard" # Actual URL after successful login (uses hyphen, not underscore)
    },
    "inventory": {
        "email": "inventory@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/inventory/index" # Placeholder - UPDATE THIS
    },
    "procurement": {
        "email": "procurement@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/procurement/dashboard" # Placeholder - UPDATE THIS
    },
    "production": {
        "email": "production@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/production/dashboard" # Placeholder - UPDATE THIS
    },
    "licensing": {
        "email": "licensing@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/licensing/dashboard" # Actual URL after successful login
    },
    "compliance": {
        "email": "compliance@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/compliance/index" # Placeholder - UPDATED
    },
    "finance": {
        "email": "finance@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/finance/index" # Placeholder - UPDATE THIS
    }
}

BASE_URL = "https://staging.mrchurros.com.my"

# --- How to extend configuration ---
# - Add new dictionaries for different environments (e.g., `DEV_CREDENTIALS`, `PROD_CREDENTIALS`).
# - Introduce new variables for other application-wide settings (e.g., API_ENDPOINTS, TIMEOUTS).
# - Ensure that sensitive information (like passwords) is handled securely in a real project
#   (e.g., environment variables, a secrets management system), not directly hardcoded.
