import pytest
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.base_api import BaseAPI
from api import USER_API_ENDPOINTS
from utils.logger import global_logger
from utils.excel_reader import ExcelReader
from utils.allure_hooks import pytest_runtest_call, pytest_runtest_teardown
from utils.flow_test_engine import FlowTestEngine
from config.settings import config

EXCEL_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', 'api_test_data.xlsx')
FLOW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', 'api_flow_test_data.xlsx')
_test_data_cache = {}
_flow_data_cache = {}

# @pytest.fixture(scope="session")
@pytest.fixture(scope="function")
def base_api():
    headers = {
        "appid": config.APPID,
        "servicecode": config.SERVICE_CODE,
        "Content-Type": "application/json"
    }
    api = BaseAPI(base_url=config.API_BASE_URL, headers=headers)
    api.set_signature_config(config.SECRET_KEY+config.SERVICE_CODE)
    yield api
    api.close()

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()

@pytest.fixture(scope="session")
def logger():
    return global_logger

def get_test_data(sheet_name: str):
    if sheet_name in _test_data_cache:
        return _test_data_cache[sheet_name]
    
    reader = ExcelReader(EXCEL_DATA_PATH)
    try:
        data = reader.get_test_data(sheet_name)
        _test_data_cache[sheet_name] = data
        return data
    finally:
        reader.close()

def get_flow_test_data():
    if _flow_data_cache:
        return _flow_data_cache.get('all_flows', [])
    
    reader = ExcelReader(FLOW_DATA_PATH)
    try:
        all_flows = reader.get_all_flow_data()
        _flow_data_cache['all_flows'] = all_flows
        return all_flows
    finally:
        reader.close()

@pytest.fixture(scope="function")
def flow_test_engine(base_api, logger):
    engine = FlowTestEngine(base_api, logger)
    yield engine

def pytest_generate_tests(metafunc):
    print(metafunc.fixturenames)    

    if "case_data" or "flow_data" not in metafunc.fixturenames:
        return
    #如果metafunc.fixturenames包含case_data执行如下代码，否则执行flow_data  
    if "case_data" in metafunc.fixturenames:        
        marker = metafunc.definition.get_closest_marker("data_sheet")
        if marker and marker.args:
            sheet_name = marker.args[0]
        else:
            sheet_name = metafunc.function.__name__
        
        data = get_test_data(sheet_name)
    else:
        flow_data = get_flow_test_data()
        
    if data or flow_data:
        # ids = [str(case.get('用例描述', f'case_{i}')) for i, case in enumerate(data)]
        # metafunc.parametrize("case_data", data, ids=ids)
        
        metafunc.parametrize("case_data", data or flow_data)
        
def pytest_sessionfinish(session, exitstatus):
    generate_report()
    global_logger.info("测试会话完成")

def generate_report():
    """生成Allure报告"""
    cmd = [
        "allure", "generate",
        config.ALLURE_RESULTS_DIR,
        "-o", config.ALLURE_REPORT_DIR,
        "--clean"
    ]
    
    print(f"生成Allure报告: {' '.join(cmd)}")
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print("Allure报告生成成功！")
        print(f"报告路径: {config.ALLURE_REPORT_DIR}")
    else:
        print("Allure报告生成失败:")
        print(result.stderr)