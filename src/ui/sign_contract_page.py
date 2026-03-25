from typing import Optional
from playwright.sync_api import Page
from .base_page import BasePage

class SignContractPage(BasePage):
    def __init__(self, page: Page, url: str = "#/subview/contractweb/contractManage/sendtemplate/sign"):
        super().__init__(page, url)
        
        self.seal_position = "text=印章位置"
        self.seal_dialog = "[role='dialog'][aria-label='印章']"
        self.confirm_button = "button:has-text('确定')"
        self.sign_now_button = "button:has-text('立即签署')"
        self.agreement_checkbox_1 = ".el-checkbox__input"
        self.agreement_checkbox_2 = ".el-checkbox.el-tooltip > .el-checkbox__input"
        self.password_input = "input[placeholder='请输入签署密码']"
        self.sign_button = "button:has-text('签署'):visible"
        self.alert_message = "div[role='alert']"
    
    def navigate_to_sign(self, contract_id: str) -> None:
        url = f"{self.url}?id={contract_id}"
        self.page.goto(url)
    
    def sign_contract(self, password: str = "1q") -> None:
        self.click_seal_position()
        self.select_first_seal()
        self.click_confirm()
        self.click_sign_now()
        self.check_agreements()
        self.enter_password(password)
        self.click_sign()
    
    def click_seal_position(self) -> None:
        self.click(self.seal_position)
        self.page.wait_for_selector(self.seal_dialog, timeout=5000)
    
    def select_first_seal(self) -> None:
        dialog = self.page.get_by_role('dialog', name='印章')
        first_seal = dialog.locator('img').first
        first_seal.click()
    
    def click_confirm(self) -> None:
        self.click(self.confirm_button,3)
    
    def click_sign_now(self) -> None:
        self.click(self.sign_now_button)
    
    def check_agreements(self) -> None:
        checkbox1 = self.page.locator(self.agreement_checkbox_1).first
        if not checkbox1.is_checked():
            checkbox1.click()
        
        checkbox2 = self.page.locator(self.agreement_checkbox_2)
        if not checkbox2.is_checked():
            checkbox2.click()
    
    def enter_password(self, password: str) -> None:
        self.fill(self.password_input, password)
    
    def click_sign(self) -> None:
        self.click(self.sign_button,2)
    
    def is_sign_success(self, timeout: int = 5000) -> bool:
        try:
            self.page.wait_for_url("**/contractList**", timeout=timeout)
            return True
        except:
            return False
    
    def get_success_message(self, timeout: int = 5000) -> str:
        try:
            self.page.wait_for_selector(self.alert_message, timeout=timeout, state="visible")
            return self.get_text(self.alert_message)
        except:
            return ""
