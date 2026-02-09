from actors.base_actor import Actor

class Finance(Actor):
    def __init__(self):
        # Use role name for clearer logs and errors.
        super().__init__("Finance")
