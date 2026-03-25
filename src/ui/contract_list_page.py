from time import sleep
import json
from typing import List, Dict, Optional
from playwright.sync_api import Page
from .base_page import BasePage
from .sign_contract_page import SignContractPage


class ContractListPage(BasePage):
    def __init__(self, page: Page, url: str = "#/subview/contractweb/contractManage/contractList"):
        super().__init__(page, url)
        
        self.expand_button = "(//div[@class='el-row'])[1]" # 展开/收起按钮
        self.contract_name_input = "input[placeholder='合同名称']"
        self.contract_create_input = "input[placeholder='请输入发起人']"
        self.signee_phone_input = "input[placeholder='请输入签署人手机号']"
        self.contract_num_input = "input[placeholder='请输入合同编号']"
        self.search_button = "button:has-text('查询')"
        self.reset_button = "button:has-text('重置')"
        self.table_body = "(//tbody)[1]"
        self.table_row = "(//tbody)[1] >> tr"       
        # self.table_body = "tbody"
        # self.table_row = "tbody >> tr"
        # self.sign_button = ".operation_item:has-text('签署')"
        self.sign_buttons = "(//tbody//td[@class='el-table_1_column_6 is-left  el-table__cell']//span[normalize-space(text())='签署'])"
        
        self.search_fields = {
            "合同名称": self.contract_name_input,
            "发起人": self.contract_create_input,
            "签署人手机号": self.signee_phone_input,
            "合同编号": self.contract_num_input,
        }
    
    def search_by_dict(self, search_params: Dict[str, str]) -> None:
        self.navigate()
        # self._wait_for_table_load()
        self.click(self.expand_button)
        
        for key, value in search_params.items():
            if not value:
                continue
                
            if key == "合同状态":
                self._select_contract_status(value)
            elif key in self.search_fields:
                self.fill(self.search_fields[key], value)
        
        self.click(self.search_button)
        self._wait_for_table_load()
    
    def search_by_json(self, json_string: str) -> None:
        search_params = json.loads(json_string)
        self.search_by_dict(search_params)
    
    def _select_contract_status(self, status: str) -> None:
        status_selector = f"//div[contains(text(),'{status}')]"
        self.click(status_selector)
        # self._wait_for_table_load()
    
    def get_search_results(self, include_contract_no: bool = True) -> List[Dict[str, str]]:
        self._wait_for_table_load()
        rows = self.page.locator(self.table_row).all()
        results = []
        # print("搜索结果行数:", len(rows))
        for row in rows:
            # print("11111111111111111111111",row)
            row.scroll_into_view_if_needed()
            cells = row.locator("td").all()
            
            if len(cells) >= 6:              
                contract_no = ""
                if include_contract_no:
                    contract_no = self._get_contract_no_from_row(row)
                
                result = {
                    "合同名称": self.get_text(cells[0].locator(".contractName_text")),
                    "合同编号": contract_no,
                    "合同来源": self.get_text(cells[1]),
                    "发起方": self.get_text(cells[2]),
                    "发送时间": self.get_text(cells[3]),
                    "状态": self.get_text(cells[4]),
                }
                results.append(result)
        
        return results
    
    def _get_contract_no_from_row(self, row) -> str:
        try:
            no_button = row.locator("span.NOclass:has-text('NO.')").first
            if no_button.count() == 0:
                return ""
            
            no_button.click()
            
            tooltip_id = no_button.get_attribute("aria-describedby")
            if tooltip_id:
                tooltip = self.page.locator(f"#{tooltip_id}")
                # tooltip.wait_for(state="visible", timeout=3000)
                contract_no = self.get_text(tooltip)
                
                no_button.click()
                
                return contract_no
        except Exception as e:
            pass
        
        return ""
    
    def get_search_result_count(self) -> int:
        return self.page.locator(self.table_row).count()
    
    
    def go_to_sign(self, search_params: Dict[str, str]) -> "SignContractPage":
        self.wait_for_loading()
        self.search_by_dict(search_params)
        
        if self.get_search_result_count() == 0:
            raise RuntimeError(f"未查询到符合条件的合同，查询条件：{json.dumps(search_params, ensure_ascii=False)}")
        
        self.click(self.sign_buttons)
        
        # sign_button_buttons = self.page.locator(self.sign_buttons).all()
        # sign_button_buttons.scroll_into_view_if_needed()
        # sign_button_buttons.click_first()
        
        # from .sign_contract_page import SignContractPage
        return SignContractPage(self.page)
    
    def go_to_sign_by_json(self, json_string: str) -> "SignContractPage":
        search_params = json.loads(json_string)
        return self.go_to_sign(search_params)
    
    def _wait_for_table_load(self, timeout: int = 10000) -> None:        
        sleep(0.5)
        self.page.wait_for_selector(self.table_body, timeout=timeout)
    
    def click_search(self) -> None:
        self.click(self.search_button)
        self._wait_for_table_load()
    
    def reset_search(self) -> None:
        self.click(self.reset_button)
        self._wait_for_table_load()
    
    def is_no_data_displayed(self) -> bool:
        no_data = self.page.locator(".no-data")
        return no_data.is_visible()
    
    def get_column_values(self, column_index: int) -> List[str]:
        column_selector = f"tbody >> tr >> td:nth-child({column_index})"
        cells = self.page.locator(column_selector).all()
        return [self.get_text(cell) for cell in cells]
    
    def get_all_contract_names(self) -> List[str]:
        return self.get_column_values(1)
    
    def get_all_creators(self) -> List[str]:
        return self.get_column_values(2)
    
    def get_all_enterprises(self) -> List[str]:
        return self.get_column_values(3)
    
    def get_all_create_times(self) -> List[str]:
        return self.get_column_values(4)
    
    def get_all_statuses(self) -> List[str]:
        return self.get_column_values(5)
