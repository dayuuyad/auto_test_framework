import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# from conftest import get_flow_test_data

@allure.feature("API流程测试")
# @pytest.mark.parametrize("flow_data", get_flow_test_data(), ids=lambda x: x['flow_name'])
def test_api_flow(flow_test_engine, flow_data, logger):
    flow_name = flow_data['flow_name']
    steps = flow_data['steps']
    
    # with allure.step(f"执行流程: {flow_name}"):
    if True:
        logger.info(f"开始执行流程: {flow_name}")
        
        result = flow_test_engine.execute_flow(flow_name, steps)
        
        assert result['success'], f"流程执行失败: {result.get('error', '未知错误')}"
        
        logger.info(f"流程执行完成: {flow_name}, 结果: {'成功' if result['success'] else '失败'}")


