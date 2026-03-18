from .base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "#login-btn"
        self.error_message = ".error-message"
    
    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
    
    def get_error_message(self) -> str:
        return self.get_text(self.error_message)
    
    def is_login_failed(self) -> bool:
        return self.is_visible(self.error_message)