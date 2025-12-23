"""
This module stores configuration data such as login credentials and base URLs.
Centralizing this data makes it easy to manage and adapt to different environments (e.g., staging, production).
"""
LOGIN_CREDENTIALS = {
    "licensee": {
        "email": "licensee@gmail.com",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/licensee/dashboard" # This should be the actual URL after successful login
    },
    "area_manager": {
        "email": "aiman.ghazali@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/area_manager/dashboard" # Placeholder - UPDATE THIS
    },
    "inventory": {
        "email": "inventory@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/inventory/dashboard" # Placeholder - UPDATE THIS
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
        "expected_dashboard_url": "https://staging.mrchurros.com.my/licensing/dashboard" # Placeholder - UPDATE THIS
    },
    "compliance": {
        "email": "compliance@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/compliance/dashboard" # Placeholder - UPDATE THIS
    },
    "finance": {
        "email": "finance@mrchurros.com.my",
        "password": "masterpassword1234",
        "expected_dashboard_url": "https://staging.mrchurros.com.my/finance/dashboard" # Placeholder - UPDATE THIS
    }
}

BASE_URL = "https://staging.mrchurros.com.my"

# --- How to extend configuration ---
# - Add new dictionaries for different environments (e.g., `DEV_CREDENTIALS`, `PROD_CREDENTIALS`).
# - Introduce new variables for other application-wide settings (e.g., API_ENDPOINTS, TIMEOUTS).
# - Ensure that sensitive information (like passwords) is handled securely in a real project
#   (e.g., environment variables, a secrets management system), not directly hardcoded.
