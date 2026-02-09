from actors.base_actor import Actor

class Production(Actor):
    def __init__(self):
        # Use role name for clearer logs and errors.
        super().__init__("Production")
