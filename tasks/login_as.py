# tasks/login_as.py
from tasks.login import Login  # your existing Login task
from config.credentials import LOGIN_CREDENTIALS

class LoginAs:
    def __init__(self, role: str):
        self.role = role

    def perform_as(self, actor):
        creds = LOGIN_CREDENTIALS[self.role]
        return Login.with_credentials(
            creds["email"],
            creds["password"]
        ).perform_as(actor)