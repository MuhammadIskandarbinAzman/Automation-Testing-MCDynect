"""
This module defines the Licensee actor.
Each specific actor embodies a user role in the system.
"""
from actors.base_actor import Actor

class Licensee(Actor):
    """
    The Licensee actor represents a user with 'Licensee' permissions.
    """
    def __init__(self):
        super().__init__("Licensee")

# --- How to create a new Actor ---
# 1. Create a new file in this directory (e.g., `area_manager.py`).
# 2. Define a class inheriting from `Actor`:
#    `class AreaManager(Actor):`
#        `def __init__(self):`
#            `super().__init__("AreaManager")`
# 3. Add a fixture for the new actor in `conftest.py` (see conftest.py notes).

