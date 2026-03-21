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
    if "case_data" in metafunc.fixturenames:
        marker = metafunc.definition.get_closest_marker("data_sheet")
        if marker and marker.args:
            sheet_name = marker.args[0]
        else:
            sheet_name = metafunc.function.__name__
        
        data = get_test_data(sheet_name)
        if data:
            # ids = [str(case.get('用例描述', f'case_{i}')) for i, case in enumerate(data)]
            # metafunc.parametrize("case_data", data, ids=ids)            
            metafunc.parametrize("case_data", data)
    
    elif "flow_data" in metafunc.fixturenames:
        data = get_flow_test_data()
        if data:
            # ids = [flow.get('flow_name', f'flow_{i}') for i, flow in enumerate(data)]
            # metafunc.parametrize("flow_data", data, ids=ids)
            metafunc.parametrize("flow_data",data)

        
def pytest_sessionfinish(session, exitstatus):

    global_logger.info("测试会话完成")

