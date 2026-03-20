import pytest
import allure
import sys
import os
from utils.json_assertion import assert_json_equals



sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from api import USER_API_ENDPOINTS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@allure.feature("用户管理")
@allure.story("用户注册")
# @pytest.mark.data_sheet("test_user_register")
def test_user_register(base_api, case_data, logger):
    case_desc = case_data.get('用例描述', '')
    test_body = case_data.get('测试body', {})
    
    with allure.step(case_desc):
        logger.info(f"开始测试: {case_desc}")
        logger.info(f"测试数据: {test_body}")
        
        response = base_api.post(USER_API_ENDPOINTS["REGISTER"], json=test_body, sign_body=True)
        logger.info(f"注册响应: {response}")

        if case_data.get('预期结果', {}):
            assert_json_equals(
                expected=case_data.get('预期结果', {}),
                actual=response,
                ignore_array_order=case_data.get('ignore_array_order', False)
            )

        # assert response.get("status") == 1
        # assert "user_id" in response

@allure.feature("用户管理")
@allure.story("用户登录")
# @pytest.mark.data_sheet("test_user_login")
def test_user_login(base_api, case_data, logger):
    case_desc = case_data.get('用例描述', '')
    test_body = case_data.get('测试body', {})
    
    with allure.step(case_desc):
        logger.info(f"开始测试: {case_desc}")
        logger.info(f"测试数据: {test_body}")
        
        response = base_api.post(USER_API_ENDPOINTS["LOGIN"], json=test_body)
        logger.info(f"登录响应: {response}")
        
        assert response.get("status") == 1  
        # assert "token" in response

@allure.feature("用户管理")
@allure.story("获取用户信息")
# @pytest.mark.data_sheet("test_get_user_info")
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
        
        assert response.get("status") == 1
        # assert response.get("user_id") == user_id
