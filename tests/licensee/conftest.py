from pathlib import Path

import pytest


def pytest_collection_modifyitems(items):
    licensee_dir = Path(__file__).resolve().parent
    for item in items:
        if licensee_dir in Path(str(item.path)).resolve().parents:
            item.add_marker(pytest.mark.licensee)
