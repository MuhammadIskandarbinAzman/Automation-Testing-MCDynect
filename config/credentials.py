"""
This module stores configuration data such as login credentials and base URLs.
Centralizing this data makes it easy to manage and adapt to different environments (e.g., staging, production).
"""
import os


def _env(key: str, default: str) -> str:
    # Central helper to read env overrides with defaults.
    return os.getenv(key, default)


BASE_URL = _env("MCDYNECT_BASE_URL", "https://staging.mrchurros.com.my")

LOGIN_CREDENTIALS = {
    "licensee": {
        # Licensee role credentials and expected landing URL.
        "email": _env("MCDYNECT_LICENSEE_EMAIL", "licensee@gmail.com"),
        "password": _env("MCDYNECT_LICENSEE_PASSWORD", "masterpassword1234"),
        "current_password": _env("MCDYNECT_LICENSEE_CURRENT_PASSWORD", "masterpassword1234"),
        "new_password": _env("MCDYNECT_LICENSEE_NEW_PASSWORD", "newmasterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_LICENSEE_DASHBOARD_URL",
            f"{BASE_URL}/licensee/dashboard",
        ),
    },
    "area_manager": {
        "email": _env("MCDYNECT_AREA_MANAGER_EMAIL", "aiman.ghazali@mrchurros.com.my"),
        "password": _env("MCDYNECT_AREA_MANAGER_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_AREA_MANAGER_DASHBOARD_URL",
            f"{BASE_URL}/area-manager/dashboard",
        ),
    },
    "inventory": {
        "email": _env("MCDYNECT_INVENTORY_EMAIL", "inventory@mrchurros.com.my"),
        "password": _env("MCDYNECT_INVENTORY_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_INVENTORY_DASHBOARD_URL",
            f"{BASE_URL}/inventory/index",
        ),
    },
    "procurement": {
        "email": _env("MCDYNECT_PROCUREMENT_EMAIL", "procurement@mrchurros.com.my"),
        "password": _env("MCDYNECT_PROCUREMENT_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_PROCUREMENT_DASHBOARD_URL",
            f"{BASE_URL}/procurement/dashboard",
        ),
    },
    "production": {
        "email": _env("MCDYNECT_PRODUCTION_EMAIL", "production@mrchurros.com.my"),
        "password": _env("MCDYNECT_PRODUCTION_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_PRODUCTION_DASHBOARD_URL",
            f"{BASE_URL}/production/dashboard",
        ),
    },
    "licensing": {
        "email": _env("MCDYNECT_LICENSING_EMAIL", "licensing@mrchurros.com.my"),
        "password": _env("MCDYNECT_LICENSING_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_LICENSING_DASHBOARD_URL",
            f"{BASE_URL}/licensing/dashboard",
        ),
    },
    "compliance": {
        "email": _env("MCDYNECT_COMPLIANCE_EMAIL", "compliance@mrchurros.com.my"),
        "password": _env("MCDYNECT_COMPLIANCE_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_COMPLIANCE_DASHBOARD_URL",
            f"{BASE_URL}/compliance/index",
        ),
    },
    "finance": {
        "email": _env("MCDYNECT_FINANCE_EMAIL", "finance@mrchurros.com.my"),
        "password": _env("MCDYNECT_FINANCE_PASSWORD", "masterpassword1234"),
        "expected_dashboard_url": _env(
            "MCDYNECT_FINANCE_DASHBOARD_URL",
            f"{BASE_URL}/finance/index",
        ),
    },
}

# --- How to extend configuration ---
# - Add new dictionaries for different environments (e.g., `DEV_CREDENTIALS`, `PROD_CREDENTIALS`).
# - Introduce new variables for other application-wide settings (e.g., API_ENDPOINTS, TIMEOUTS).
# - Ensure that sensitive information (like passwords) is handled securely in a real project
#   (e.g., environment variables, a secrets management system), not directly hardcoded.
