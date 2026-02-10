"""
This module stores configuration data such as login credentials and base URLs.
Centralizing this data makes it easy to manage and adapt to different environments (e.g., staging, production).
"""
import os


def _env(key: str) -> str:
    # Central helper to read required env vars.
    value = os.getenv(key)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


BASE_URL = _env("MCDYNECT_BASE_URL")

LOGIN_CREDENTIALS = {
    "licensee": {
        # Licensee role credentials and expected landing URL.
        "email": _env("MCDYNECT_LICENSEE_EMAIL"),
        "password": _env("MCDYNECT_LICENSEE_PASSWORD"),
        "current_password": _env("MCDYNECT_LICENSEE_CURRENT_PASSWORD"),
        "new_password": _env("MCDYNECT_LICENSEE_NEW_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_LICENSEE_DASHBOARD_URL"),
    },
    "area_manager": {
        "email": _env("MCDYNECT_AREA_MANAGER_EMAIL"),
        "password": _env("MCDYNECT_AREA_MANAGER_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_AREA_MANAGER_DASHBOARD_URL"),
    },
    "inventory": {
        "email": _env("MCDYNECT_INVENTORY_EMAIL"),
        "password": _env("MCDYNECT_INVENTORY_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_INVENTORY_DASHBOARD_URL"),
    },
    "procurement": {
        "email": _env("MCDYNECT_PROCUREMENT_EMAIL"),
        "password": _env("MCDYNECT_PROCUREMENT_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_PROCUREMENT_DASHBOARD_URL"),
    },
    "production": {
        "email": _env("MCDYNECT_PRODUCTION_EMAIL"),
        "password": _env("MCDYNECT_PRODUCTION_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_PRODUCTION_DASHBOARD_URL"),
    },
    "licensing": {
        "email": _env("MCDYNECT_LICENSING_EMAIL"),
        "password": _env("MCDYNECT_LICENSING_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_LICENSING_DASHBOARD_URL"),
    },
    "compliance": {
        "email": _env("MCDYNECT_COMPLIANCE_EMAIL"),
        "password": _env("MCDYNECT_COMPLIANCE_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_COMPLIANCE_DASHBOARD_URL"),
    },
    "finance": {
        "email": _env("MCDYNECT_FINANCE_EMAIL"),
        "password": _env("MCDYNECT_FINANCE_PASSWORD"),
        "expected_dashboard_url": _env("MCDYNECT_FINANCE_DASHBOARD_URL"),
    },
}

# --- How to extend configuration ---
# - Add new dictionaries for different environments (e.g., `DEV_CREDENTIALS`, `PROD_CREDENTIALS`).
# - Introduce new variables for other application-wide settings (e.g., API_ENDPOINTS, TIMEOUTS).
# - Ensure that sensitive information (like passwords) is handled securely in a real project
#   (e.g., environment variables, a secrets management system), not directly hardcoded.
