from .base_actor import Actor

class Licensee(Actor):
    def __init__(self, email: str = None, password: str = None):
        super().__init__()
        self.email = email
        self.password = password