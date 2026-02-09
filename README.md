# MCDynect Automation

End-to-end UI test automation for MCDynect using Playwright and the Screenplay Pattern.

## Overview
This project models user roles as Actors who perform Tasks and ask Questions about the UI.  
Selectors live in `ui/`, business actions in `tasks/`, and assertions in `questions/`.

## Tech Stack
- Python
- Pytest
- Playwright (sync API)

## Project Structure
- `abilities/` - Actor abilities (e.g., `BrowseTheWeb`) wrapping Playwright actions
- `actors/` - Role-based actors (Licensee, AreaManager, etc.)
- `tasks/` - Business actions (e.g., `Login`)
- `questions/` - UI queries for assertions
- `ui/` - Centralized UI locators
- `config/` - Base URL and credentials (supports env overrides)
- `tests/` - Pytest test scenarios
- `test_runs/` - Timestamped screenshots and run artifacts

## Quick Start
1. Create and activate a virtual environment.
2. Install dependencies.
3. Install Playwright browsers.
4. Run tests.

Example:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
pytest
```

## Configuration
Configuration lives in `config/credentials.py` and can be overridden with environment variables.

Common variables:
- `MCDYNECT_BASE_URL`
- `MCDYNECT_LICENSEE_EMAIL`
- `MCDYNECT_LICENSEE_PASSWORD`
- `MCDYNECT_LICENSEE_DASHBOARD_URL`

Each role has its own set of `MCDYNECT_<ROLE>_*` variables.

## Writing Tests (Screenplay Pattern)
Example:
```python
def test_licensee_can_log_in(the_licensee):
    the_licensee.attempts_to(Login.with_credentials(email, password))
    assert WelcomeMessage.is_visible_to(the_licensee)
```

## Notes
- Screenshots are taken automatically after each test and saved under `test_runs/<timestamp>/screenshots`.
- `pytest.ini` excludes the legacy `Automation-Testing-MCDynect/` folder from discovery.

