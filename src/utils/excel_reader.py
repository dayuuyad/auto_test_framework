import openpyxl
import json
from typing import Dict, List, Optional
from utils.logger import global_logger

class ExcelReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = None
        self.logger = global_logger
    
    def load_workbook(self) -> None:
        try:
            self.workbook = openpyxl.load_workbook(self.file_path)
            self.logger.info(f"成功加载Excel文件: {self.file_path}")
        except Exception as e:
            self.logger.error(f"加载Excel文件失败: {e}")
            raise
    
    def get_sheet_data(self, sheet_name: str) -> List[Dict]:
        if not self.workbook:
            self.load_workbook()
        
        if sheet_name not in self.workbook.sheetnames:
            self.logger.warning(f"Sheet '{sheet_name}' 不存在")
            return []
        
        sheet = self.workbook[sheet_name]
        data = []
        
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            
            row_data = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    row_data[headers[i]] = value
            
            data.append(row_data)
        
        self.logger.info(f"从Sheet '{sheet_name}' 读取到 {len(data)} 条数据")
        return data
    
    def parse_test_body(self, body_str: str) -> Dict:
        if not body_str:
            return {}
        
        try:
            if isinstance(body_str, str):
                return json.loads(body_str)
            elif isinstance(body_str, dict):
                return body_str
            else:
                return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}, 原始数据: {body_str}")
            return {}
    
    def filter_executable_cases(self, data: List[Dict]) -> List[Dict]:
        executable_cases = []
        
        for case in data:
            is_executable = case.get('用例是否执行', 'FALSE')
            
            if isinstance(is_executable, str):
                is_executable = is_executable.upper().strip()
            
            if is_executable == True or is_executable == 'TRUE':
                if '测试body' in case:
                    case['测试body'] = self.parse_test_body(case['测试body'])
                executable_cases.append(case)
        
        self.logger.info(f"过滤后可执行的用例数: {len(executable_cases)}")
        return executable_cases
    
    def get_test_data(self, sheet_name: str) -> List[Dict]:
        data = self.get_sheet_data(sheet_name)
        return self.filter_executable_cases(data)
    
    def close(self) -> None:
        if self.workbook:
            self.workbook.close()
            self.logger.info("关闭Excel文件")

def get_excel_data(file_path: str, sheet_name: str) -> List[Dict]:
    reader = ExcelReader(file_path)
    try:
        data = reader.get_test_data(sheet_name)
        return data
    finally:
        reader.close()