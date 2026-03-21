import allure
import json
import pytest
from typing import Optional, Dict, Any


def attach_request_response_to_allure(request_data: Optional[Dict[str, Any]], 
                                    response_data: Optional[Dict[str, Any]]) -> None:
    """将请求和响应数据附加到Allure报告"""
    
    if request_data:
        # 附加请求信息
        allure.dynamic.description(f"**请求方法:** {request_data.get('method', 'N/A')}\n"
                                   f"**请求URL:** {request_data.get('url', 'N/A')}\n"
                                   f"**状态码:** {response_data.get('status_code', 'N/A') if response_data else 'N/A'}")
        
        # # 附加请求头
        # if request_data.get('headers'):
        #     allure.attach(
        #         json.dumps(dict(request_data['headers']), indent=2, ensure_ascii=False),
        #         name="请求头",
        #         attachment_type=allure.attachment_type.JSON
        #     )
        
        # 附加请求参数
        if request_data.get('params'):
            allure.attach(
                json.dumps(request_data['params'], indent=2, ensure_ascii=False),
                name="请求参数",
                attachment_type=allure.attachment_type.JSON
            )
        
        # 附加请求体
        request_body = None
        if request_data.get('json'):
            request_body = request_data['json']
        elif request_data.get('data'):
            request_body = request_data['data']
        
        if request_body:
            allure.attach(
                json.dumps(request_body, indent=2, ensure_ascii=False),
                name="请求体",
                attachment_type=allure.attachment_type.JSON
            )
    
    if response_data:
        # # 附加响应头
        # if response_data.get('headers'):
        #     allure.attach(
        #         json.dumps(dict(response_data['headers']), indent=2, ensure_ascii=False),
        #         name="响应头",
        #         attachment_type=allure.attachment_type.JSON
        #     )
        
        # 附加响应体
        response_body = response_data.get('json') or response_data.get('body')
        if response_body:
            if isinstance(response_body, dict):
                allure.attach(
                    json.dumps(response_body, indent=2, ensure_ascii=False),
                    name="响应体",
                    attachment_type=allure.attachment_type.JSON
                )
            else:
                allure.attach(
                    str(response_body),
                    name="响应体",
                    attachment_type=allure.attachment_type.TEXT
                )


def attach_request_response_callback(request_data: Optional[Dict[str, Any]], 
                                     response_data: Optional[Dict[str, Any]]) -> None:
    """回调函数：实时将请求和响应数据附加到Allure报告"""
    url = request_data.get('url', 'N/A') if request_data else 'N/A'
    
    with allure.step(f"调用接口: {url}"):
        attach_request_response_to_allure(request_data, response_data)


def pytest_runtest_call(item):
    """在每个测试用例执行时调用的hook"""
    if hasattr(item, 'funcargs') and 'base_api' in item.funcargs:
        base_api_fixture = item.funcargs.get('base_api')
        
        if base_api_fixture:
            base_api_fixture.clear_request_response_data()
            base_api_fixture.set_request_callback(attach_request_response_callback)


def pytest_runtest_teardown(item, nextitem):
    """在每个测试用例执行后调用的hook"""
    if hasattr(item, 'funcargs') and 'base_api' in item.funcargs:
        base_api_fixture = item.funcargs.get('base_api')
        
        if base_api_fixture:
            base_api_fixture.clear_request_callback()