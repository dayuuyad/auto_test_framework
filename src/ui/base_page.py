from playwright.sync_api import Page, Locator
from typing import Optional, Tuple

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str) -> None:
        self.page.goto(url)
    
    def click(self, selector: str) -> None:
        self.page.click(selector)
    
    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)
    
    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
    
    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, path: str) -> None:
        self.page.screenshot(path=path)
    
    def get_title(self) -> str:
        return self.page.title()
    
    def get_url(self) -> str:
        return self.page.url()