from typing import Dict, Optional, List
from playwright.sync_api import Page
from .base_page import BasePage
from ui.send_contract_page import SendContractPage



class CreateContractPage(BasePage):
    def __init__(self, page: Page, url: str = "#/subview/contractweb/contractManage/sendtemplate/createContract"):
        super().__init__(page, url)
        
        self.business_type_input = "input[placeholder='请选择业务类型']"
        self.contract_title_input = "input[placeholder='请输入合同标题']"
        self.file_format_input = "input[disabled]"
        self.expiry_time_input = "input[type='number']"
        self.effective_date_input = "input[placeholder='请选择生效日期']"
        self.add_file_button = "button:has-text('添加文件')"
        # self.add_internal_employee_button = "button:has-text('添加内部员工')"
        self.add_internal_employee_button = ".filepage-content-flex-child:has-text('添加内部员工')"
        self.add_enterprise_signer_button = "button:has-text('添加企业签署方')"
        self.add_personal_signer_button = "button:has-text('添加个人签署方')"
        self.next_button = "button:has-text('下一步')"
        self.cancel_button = "button:has-text('取消')"
        self.sign_settings_button = "text=签署设置"
        self.delete_button = "text=删除"        
        self.save_button = "//button/span[text()='保存']/.."        
        self.confirm_button = "button:has-text('确定')"
        self.alert_message = "div[role='alert']"
        self.dialog_close_button = "button[aria-label='Close']"
        self.employee_checkbox = ".el-checkbox__input"
        self.file_list = "tbody >> tr"
        self.signer_list = "#userFileList"
    
    def create_contract(self, contract_info: Dict[str, str]) -> SendContractPage:
        self.navigate()
        
        if "业务类型" in contract_info:
            self.select_business_type(contract_info["业务类型"])
            self.wait_for_loading()        

        if "合同标题" in contract_info:
            self.fill_contract_title(contract_info["合同标题"])

        # self.wait_for_time()
        if "文件路径" in contract_info:
            self.upload_file(contract_info["文件路径"])
        
        if "签署方" in contract_info:
            self.add_signers(contract_info["签署方"])       
        
        self.click_next()
        self.wait_for_url_change()
            # 获取 hash 部分（包含 #）
        hash_part = self.page.evaluate("() => window.location.hash")
        print(hash_part) 
        send_contract_page = SendContractPage(self.page,url=hash_part)
        return send_contract_page
    
    def select_business_type(self, business_type: str) -> None:
        self.click(self.business_type_input)
        self.click(f"li:has-text('{business_type}')")
    
    def fill_contract_title(self, title: str) -> None:
        print("合同标题："+title)
        self.fill(self.contract_title_input, title)
    
    def upload_file(self, file_path: str) -> None:
        with self.page.expect_file_chooser() as fc_info:
            self.click(self.add_file_button)
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)
        # self.page.wait_for_selector(f"{self.file_list} >> td", timeout=5000)
    
    def add_internal_employee(self, employee_name: str) -> None:
        self.click(self.add_internal_employee_button)
        # self.click(self.cancel_button,2)
        # self.click(self.add_internal_employee_button)
        # self.page.wait_for_selector(f".el-tree-node__content:has-text('{employee_name}')", timeout=5000)        
        
        self.click(f".el-tree-node__content:has-text('{employee_name}')")
        # self.click(self.employee_checkbox)
        # self.wait_for_time(5000)

        self.click(self.save_button)
    
    def add_enterprise_signer(self, enterprise_name: str) -> None:
        self.click(self.add_enterprise_signer_button)
        # self.page.wait_for_selector("div[role='dialog']", timeout=5000)
    
    def add_personal_signer(self, name: str, phone: str) -> None:
        self.click(self.add_personal_signer_button)
        # self.page.wait_for_selector("div[role='dialog']", timeout=5000)
    
    def add_signers(self, signers: List[Dict[str, str]]) -> None:
        for signer in signers:
            signer_type = signer.get("类型", "")
            
            if signer_type == "内部员工":
                self.add_internal_employee(signer.get("姓名", ""))
            elif signer_type == "企业签署方":
                self.add_enterprise_signer(signer.get("企业名称", ""))
            elif signer_type == "个人签署方":
                self.add_personal_signer(signer.get("姓名", ""), signer.get("手机号", ""))
    
    def click_next(self) -> None:
        self.click(self.next_button)
    
    def click_cancel(self) -> None:
        self.click(self.cancel_button)
    
    def configure_sign_settings(self, receive_notification: bool = True, specify_position: bool = True) -> None:
        self.click(self.sign_settings_button)
        
        notification_option = "是" if receive_notification else "否"
        self.click(f"label:has-text('{notification_option}') input[type='radio']")
        
        position_option = "是" if specify_position else "否"
        self.click(f"label:has-text('{position_option}') input[type='radio']")
        
        self.click(self.confirm_button)
    
    def delete_signer(self) -> None:
        self.click(self.delete_button)
    
    def get_uploaded_files(self) -> List[str]:
        files = self.page.locator(self.file_list).all()
        file_names = []
        for file in files:
            name = self.get_text(file.locator("td:nth-child(1)"))
            file_names.append(name)
        return file_names
    
    def get_signers(self) -> List[Dict[str, str]]:
        signers = []
        signer_elements = self.page.locator(f"{self.signer_list} >> .el-card").all()
        
        for element in signer_elements:
            signer_type = self.get_text(element.locator(".el-tag"))
            name = self.get_text(element.locator("input[placeholder*='签署人姓名']"))
            phone = self.get_text(element.locator("input[placeholder='手机号']"))
            
            signers.append({
                "类型": signer_type,
                "姓名": name,
                "手机号": phone
            })
        
        return signers
    
    def is_file_uploaded(self, file_name: str) -> bool:
        files = self.get_uploaded_files()
        return file_name in files
    



    def get_success_message(self, timeout: int = 5000) -> str:
        try:
            self.page.wait_for_selector(self.alert_message, timeout=timeout, state="visible")
            return self.get_text(self.alert_message)
        except:
            return ""
    
    def is_submit_success(self, timeout: int = 5000) -> bool:
        message = self.get_success_message(timeout)
        return "提交数据成功" in message
    
    # def wait_for_page_load(self, timeout: int = 10000) -> None:
    #     self.wait_for_selector(self.business_type_input, timeout=timeout)
    
    def reset_form(self) -> None:
        self.click_cancel()
