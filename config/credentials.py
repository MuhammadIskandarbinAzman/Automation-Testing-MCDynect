"""
This module stores configuration data such as login credentials and base URLs.
Centralizing this data makes it easy to manage and adapt to different environments (e.g., staging, production).
"""
import os
from collections.abc import Mapping
from pathlib import Path


def _load_dotenv() -> None:
    """
    Load .env from project root into process env (without overriding existing vars).
    This keeps IDE test discovery and direct `pytest` runs consistent.
    """
    for env_name in (".env", ".env.example"):
        env_path = Path(__file__).resolve().parents[1] / env_name
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            # Remove optional wrapping quotes.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            os.environ.setdefault(key, value)


_load_dotenv()


def _env(key: str) -> str:
    # Central helper to read required env vars.
    value = os.getenv(key)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def get_base_url() -> str:
    return _env("MCDYNECT_BASE_URL")


def get_login_credentials() -> dict[str, dict[str, str]]:
    return {
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


def get_admin_credentials() -> dict[str, str]:
    """
    Load admin credentials only when admin tests need them.

    Keeping this separate prevents normal role tests from requiring admin env vars.
    """
    base_url = get_base_url()
    return {
        "email": _env("MCDYNECT_ADMIN_EMAIL"),
        "password": _env("MCDYNECT_ADMIN_PASSWORD"),
        "expected_dashboard_url": os.getenv(
            "MCDYNECT_ADMIN_DASHBOARD_URL",
            f"{base_url}/admin/dashboard",
        ),
    }


def get_impersonation_targets() -> dict[str, dict[str, str]]:
    """
    Return impersonation targets for admin smoke tests.

    `MCDYNECT_IMPERSONATE_ROLES` can limit the run, for example:
    `licensee,finance,licensing`.
    """
    base_url = get_base_url()
    all_targets = {
        "licensee": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_LICENSEE_SEARCH", "licensee"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_LICENSEE_URL",
                f"{base_url}/licensee/dashboard",
            ),
        },
        "finance": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_FINANCE_SEARCH", "finance"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_FINANCE_URL",
                f"{base_url}/finance/index",
            ),
        },
        "licensing": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_LICENSING_SEARCH", "licensing"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_LICENSING_URL",
                f"{base_url}/licensing/dashboard",
            ),
        },
        "production": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_PRODUCTION_SEARCH", "production"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_PRODUCTION_URL",
                f"{base_url}/production/dashboard",
            ),
        },
        "compliance": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_COMPLIANCE_SEARCH", "compliance"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_COMPLIANCE_URL",
                f"{base_url}/compliance/index",
            ),
        },
        "procurement": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_PROCUREMENT_SEARCH", "procurement"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_PROCUREMENT_URL",
                f"{base_url}/procurement/dashboard",
            ),
        },
        "inventory": {
            "search": os.getenv("MCDYNECT_IMPERSONATE_INVENTORY_SEARCH", "inventory"),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_INVENTORY_URL",
                f"{base_url}/inventory/index",
            ),
        },
        "area_manager": {
            "search": os.getenv(
                "MCDYNECT_IMPERSONATE_AREA_MANAGER_SEARCH",
                "area manager",
            ),
            "expected_url": os.getenv(
                "MCDYNECT_IMPERSONATE_AREA_MANAGER_URL",
                f"{base_url}/area-manager/dashboard",
            ),
        },
    }
    selected_roles = os.getenv(
        "MCDYNECT_IMPERSONATE_ROLES",
        (
            "licensee,area_manager,inventory,procurement,production,"
            "licensing,compliance,finance"
        ),
    )
    roles = [role.strip() for role in selected_roles.split(",") if role.strip()]
    unknown_roles = [role for role in roles if role not in all_targets]
    if unknown_roles:
        available_roles = ", ".join(sorted(all_targets))
        raise RuntimeError(
            "Unknown MCDYNECT_IMPERSONATE_ROLES value(s): "
            f"{', '.join(unknown_roles)}. Available roles: {available_roles}"
        )
    return {role: all_targets[role] for role in roles}


class _LazyEnvValue:
    def __init__(self, loader):
        self._loader = loader

    def _value(self) -> str:
        return self._loader()

    def __str__(self) -> str:
        return self._value()

    def __repr__(self) -> str:
        return repr(self._value())

    def __format__(self, format_spec: str) -> str:
        return format(self._value(), format_spec)


class _LazyCredentials(Mapping):
    def __getitem__(self, key):
        return get_login_credentials()[key]

    def __iter__(self):
        return iter(get_login_credentials())

    def __len__(self) -> int:
        return len(get_login_credentials())


BASE_URL = _LazyEnvValue(get_base_url)
LOGIN_CREDENTIALS = _LazyCredentials()

# --- How to extend configuration ---
# - Add new dictionaries for different environments (e.g., `DEV_CREDENTIALS`, `PROD_CREDENTIALS`).
# - Introduce new variables for other application-wide settings (e.g., API_ENDPOINTS, TIMEOUTS).
# - Ensure that sensitive information (like passwords) is handled securely in a real project
#   (e.g., environment variables, a secrets management system), not directly hardcoded.
