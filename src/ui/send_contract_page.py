from typing import Dict, Optional, List
from warnings import simplefilter
from playwright.sync_api import Page, SourceLocation
from .base_page import BasePage
from .contract_list_page import ContractListPage



class SendContractPage(BasePage):
    def __init__(self, page: Page, url: str = "#/subview/contractweb/contractManage/sendtemplate/sendContract"):
        super().__init__(page, url)
        
        self.back_button = "text=返回"
        self.send_button = "button:has-text('发送')"
        self.previous_button = "button:has-text('上一步')"
        self.file_list_item = ".file-list >> li"
        self.signer_list_item = ".signer-list >> li"
        self.seal_control = "text=印章"
        self.date_control = "text=日期"
        self.signature_control = "text=经办人签名"
        self.legal_representative_seal = "text=法定代表人章"
        self.cross_page_seal = "text=骑缝章"
        self.text_control = "text=文本"
        self.pdf_area = ".edit_center, canvas"
        self.alert_message = "div[role='alert']"
        self.signer_name = ".signer-name"
    
    # def navigate(self, contract_id: str) -> None:
    #     url = f"{self.url}?id={contract_id}&successCallbackRouteName"
    #     self.page.goto(url)
     
    
    def send_contract(self, seal_position: Optional[Dict[str, int]] = None) -> ContractListPage:
        # self.navigate("http://localhost:8888/#/subview/contractweb/contractManage/sendtemplate/sendContract?id=244815169606123532&successCallbackRouteName")
        self.wait_for_loading()
        
        if seal_position:
            self.drag_seal_to_position(seal_position)
        else:
            self.drag_seal_to_pdf()
            # self.drag_seal_to_position({"x": 816, "y": 400})        
        self.click_send()
        return ContractListPage(self.page)
    
    def drag_seal_to_pdf(self) -> None:
        seal_element = self.page.locator(self.seal_control).nth(1)
        pdf_area = self.page.locator(self.pdf_area).first
        
        seal_box = seal_element.bounding_box()
        pdf_box = pdf_area.bounding_box()
        print("seal_box:", seal_box)
        print("pdf_box:", pdf_box)
        print(pdf_box['x'] + pdf_box['width'] / 2, pdf_box['y'] + pdf_box['height'] / 2)  

        if seal_box and pdf_box:
            self.page.mouse.move(seal_box['x'] + seal_box['width'] / 2, seal_box['y'] + seal_box['height'] / 2)
            self.page.mouse.down()
            self.page.mouse.move(pdf_box['x'] + pdf_box['width'] / 2, pdf_box['y'] + pdf_box['height'] / 2, steps=10)
            self.page.mouse.up()
    
    def drag_seal_to_position(self, position: Dict[str, int]) -> None:
        seal_element = self.page.locator(self.seal_control).nth(1)
        pdf_area = self.page.locator(self.pdf_area).first
        
        seal_box = seal_element.bounding_box()
        pdf_box = pdf_area.bounding_box()        

        if seal_box and pdf_box:
            self.page.mouse.move(seal_box['x'] + seal_box['width'] / 2, seal_box['y'] + seal_box['height'] / 2)
            self.page.mouse.down()
            self.page.mouse.move(position['x'], position['y'], steps=10)
            self.page.mouse.up()
    
    def drag_control_to_pdf(self, control_type: str) -> None:
        control_locator = f"text={control_type}"
        control_element = self.page.locator(control_locator).nth(1)
        pdf_area = self.page.locator(self.pdf_area).first
        
        control_box = control_element.bounding_box()
        pdf_box = pdf_area.bounding_box()
        
        if control_box and pdf_box:
            self.page.mouse.move(control_box['x'] + control_box['width'] / 2, control_box['y'] + control_box['height'] / 2)
            self.page.mouse.down()
            self.page.mouse.move(pdf_box['x'] + pdf_box['width'] / 2, pdf_box['y'] + pdf_box['height'] / 2, steps=10)
            self.page.mouse.up()
    
    def click_send(self) -> None:
        self.click(self.send_button)
    
    def click_back(self) -> None:
        self.click(self.back_button)
    
    def click_previous(self) -> None:
        self.click(self.previous_button)
    
    def select_file(self, file_index: int = 0) -> None:
        files = self.page.locator(self.file_list_item).all()
        if file_index < len(files):
            files[file_index].click()
    
    def select_signer(self, signer_index: int = 0) -> None:
        signers = self.page.locator(self.signer_list_item).all()
        if signer_index < len(signers):
            signers[signer_index].click()
    
    def get_files(self) -> List[str]:
        files = self.page.locator(self.file_list_item).all()
        file_names = []
        for file in files:
            name = self.get_text(file)
            file_names.append(name)
        return file_names
    
    def get_signers(self) -> List[str]:
        signers = self.page.locator(self.signer_list_item).all()
        signer_names = []
        for signer in signers:
            name = self.get_text(signer.locator(self.signer_name))
            signer_names.append(name)
        return signer_names
    
    def is_success_message_displayed(self, timeout: int = 5000) -> bool:
        try:
            self.page.wait_for_selector(self.alert_message, timeout=timeout, state="visible")
            return True
        except:
            return False
    
    def get_success_message(self, timeout: int = 5000) -> str:
        try:
            self.page.wait_for_selector(self.alert_message, timeout=timeout, state="visible")
            return self.get_text(self.alert_message)
        except:
            return ""
    
    def is_send_success(self, timeout: int = 5000) -> bool:
        message = self.get_success_message(timeout)
        return "保存成功" in message or "发送成功" in message
    
    def is_send_button_disabled(self) -> bool:
        send_button = self.page.locator(self.send_button)
        return send_button.is_disabled()
    
    def get_page_title(self) -> str:
        return self.page.title()
