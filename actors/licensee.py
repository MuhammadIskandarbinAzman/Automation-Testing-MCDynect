from .base_actor import Actor

class Licensee(Actor):
    def __init__(self, email: str = None, password: str = None):
        # Keep email/password on the actor for tasks like password updates.
        super().__init__()
        self.email = email
        self.password = password
