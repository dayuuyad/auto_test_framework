from playwright.sync_api import Page, Locator
from typing import Optional, Tuple
from config.settings import config

class BasePage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = config.UI_BASE_URL + url
        self.alert_message = "div[role='alert']"

    def navigate(self, url: str = None) -> None:
        if url:
            self.page.goto(url)
        else:
            self.page.goto(self.url)    

    def click(self, selector: str, index: int = 0) -> None:
        print("11111111111111111111111111111111111111111111111",selector)
        # self.page.click(selector, index=index)
        self.page.locator(selector).nth(index).click()

    
    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)
    
    # def get_text(self, selector: str) -> str:
    #     return self.page.inner_text(selector).strip()
    
    def get_text(self, selector) -> str:
        if isinstance(selector, Locator):
            return selector.inner_text().strip()
        return self.page.inner_text(selector).strip()    


    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

   
    def wait_for_selector_disappear(self, selector: str, timeout: int = 30000) -> None:
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)


    def wait_for_loading(self, timeout: int = 30000) -> None:        
        self.wait_for_selector_disappear("div[class='el-loading-spinner']", timeout=timeout)

    def take_screenshot(self, path: str) -> None:
        self.page.screenshot(path=path)
    
    def get_title(self) -> str:
        return self.page.title()
    
    def get_url(self) -> str:
        return self.page.url()

    def get_alert_message(self, timeout: int = None) -> str:
        if timeout:
            self.page.wait_for_selector(self.alert_message, timeout=timeout)
        return self.get_text(self.alert_message)
      

    def wait_for_url_change(self) -> None:        
        self.page.wait_for_url(lambda url: url != self.url)

    
    def wait_for_time(self, timeout: int = 30000) -> None:
        self.page.wait_for_timeout(timeout)