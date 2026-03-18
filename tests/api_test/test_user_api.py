import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from api import USER_API_ENDPOINTS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from conftest import get_test_data

def get_case_ids(data):
    return [case.get('用例描述', f'case_{i}') for i, case in enumerate(data)]

@allure.feature("用户管理")
@allure.story("用户注册")
# @pytest.mark.parametrize("case_data", get_test_data("test_user_register"), ids=get_case_ids(get_test_data("test_user_register")))
@pytest.mark.parametrize("case_data", get_test_data("test_user_register"))
def test_user_register(base_api, case_data, logger):
    case_desc = case_data.get('用例描述', '')
    test_body = case_data.get('测试body', {})
    
    with allure.step(case_desc):
        logger.info(f"开始测试: {case_desc}")
        logger.info(f"测试数据: {test_body}")
        
        response = base_api.post(USER_API_ENDPOINTS["REGISTER"], json=test_body)
        logger.info(f"注册响应: {response}")
        
        assert response.get("status") == "success"
        assert "user_id" in response

@allure.feature("用户管理")
@allure.story("用户登录")
@pytest.mark.parametrize("case_data", get_test_data("test_user_login"), ids=get_case_ids(get_test_data("test_user_login")))
def test_user_login(base_api, case_data, logger):
    case_desc = case_data.get('用例描述', '')
    test_body = case_data.get('测试body', {})
    
    with allure.step(case_desc):
        logger.info(f"开始测试: {case_desc}")
        logger.info(f"测试数据: {test_body}")
        
        response = base_api.post(USER_API_ENDPOINTS["LOGIN"], json=test_body)
        logger.info(f"登录响应: {response}")
        
        assert response.get("status") == "success"
        assert "token" in response

@allure.feature("用户管理")
@allure.story("获取用户信息")
@pytest.mark.parametrize("case_data", get_test_data("test_get_user_info"), ids=get_case_ids(get_test_data("test_get_user_info")))
def test_get_user_info(base_api, case_data, logger):
    case_desc = case_data.get('用例描述', '')
    test_body = case_data.get('测试body', {})
    
    with allure.step(case_desc):
        logger.info(f"开始测试: {case_desc}")
        logger.info(f"测试数据: {test_body}")
        
        user_id = test_body.get('user_id', 1)
        endpoint = USER_API_ENDPOINTS["GET_USER_INFO"].format(user_id=user_id)
        
        response = base_api.get(endpoint)
        logger.info(f"获取用户信息响应: {response}")
        
        assert response.get("status") == "success"
        assert response.get("user_id") == user_id