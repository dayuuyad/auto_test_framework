import pytest
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.base_api import BaseAPI
from api import USER_API_ENDPOINTS
from utils.logger import global_logger
from utils.excel_reader import ExcelReader
from utils.allure_hooks import pytest_runtest_call, pytest_runtest_teardown
from config.settings import config

EXCEL_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', 'api_test_data.xlsx')
_test_data_cache = {}

@pytest.fixture(scope="session")
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

def pytest_generate_tests(metafunc):
    if "case_data" not in metafunc.fixturenames:
        return
    
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
        