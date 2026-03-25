import base64
from time import sleep
import ddddocr
from .base_page import BasePage
from playwright.sync_api import Page, expect

class LoginPage(BasePage):
    def __init__(self, page: Page, url: str = "#/signMountApp/login"):
        super().__init__(page, url)
        self.username_input = "input[placeholder='请输入您的手机号/邮箱/账号名']"
        self.password_input = "input[placeholder='请输入密码']"
        self.captcha_input = "input[placeholder='请输入验证码']"
        self.captcha_image = "img[class='code']"
        self.checkbox = "span[class='el-checkbox__input']"
        self.login_button = "button[type='button']"

    
    def login(self, username: str, password: str, auto_captcha: bool = True, max_retries: int = 3) -> bool:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.checkbox)
        
        for attempt in range(max_retries):
            if auto_captcha:
                captcha_text = self.recognize_captcha()
                self.fill(self.captcha_input, captcha_text)
                # self.fill(self.captcha_input, "666666")

            
            self.click(self.login_button)
            
            result = self._wait_for_login_result()
            
            if result == "success":
                return True
            elif result == "图形验证码错误":
                self.refresh_captcha()
                self.wait_for_selector_disappear(self.alert_message)
                continue
            else:
                return False
        
        return False
    
    def _wait_for_login_result(self, alert_timeout: int = 3000, url_timeout: int = 10000) -> str:
        try:
            alert_message = self.get_alert_message(timeout=alert_timeout)        
            if alert_message:         
                return alert_message
        except:
            pass

        success_url = "/subview/contractweb/contractManage/contractList"
        success_pattern = f"**{success_url}**"        
        try:
            self.page.wait_for_url(success_pattern, timeout=url_timeout)
            return "success"
        except:
            pass
        
        return "unknown"


    def is_login_success(self) -> bool:
        return "/subview/contractweb/contractManage/contractList" in self.page.url

    
    def is_login_failed(self) -> bool:
        return self.get_alert_message() == "登录失败"

    def is_checkbox_checked(self) -> bool:
        return self.is_checked(self.checkbox)
    
    def refresh_captcha(self) -> None:
        self.click(self.captcha_image)
        sleep(0.5)
    
    def recognize_captcha(self) -> str:
        src = self.page.locator(self.captcha_image).get_attribute('src')
        if src and src.startswith('data:image'):
            base64_data = src.split(',', 1)[1]
            image_bytes = base64.b64decode(base64_data)
            ocr = ddddocr.DdddOcr(show_ad=False)
            return ocr.classification(image_bytes)
        return ''