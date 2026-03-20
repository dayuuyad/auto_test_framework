import json
from typing import Any, Dict, List, Optional
from utils.context_manager import ContextManager
from utils.param_replacer import ParamReplacer
from utils.response_extractor import ResponseExtractor
from utils.logger import global_logger
from utils.json_assertion import assert_json_equals
from utils.json_utils import safe_parse_json


class FlowTestEngine:
    def __init__(self, base_api, logger=None):
        self.base_api = base_api
        self.logger = logger or global_logger
        self.context = ContextManager()
        self.param_replacer = ParamReplacer(self.context)
        self.response_extractor = ResponseExtractor()
    
    def execute_flow(self, flow_name: str, steps: List[Dict]) -> Dict:
        self.logger.info(f"开始执行流程: {flow_name}")
        self.context.clear()
        
        result = {
            "flow_name": flow_name,
            "success": True,
            "steps": [],
            "error": None
        }
        
        try:
            for index, step in enumerate(steps, 1):
                step_result = self.execute_step(step, index)
                result["steps"].append(step_result)
                
                if not step_result["success"]:
                    result["success"] = False
                    result["error"] = f"步骤{index}执行失败: {step_result.get('error', '未知错误')}"
                    break
        
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            self.logger.error(f"流程执行异常: {e}")
        
        self.logger.info(f"流程执行完成: {flow_name}, 结果: {'成功' if result['success'] else '失败'}")
        return result
    
    def execute_step(self, step: Dict, step_index: int) -> Dict:
        url = step.get("接口地址", "")
        params_str = step.get("请求参数（JSON）", "{}")
        expected_str = step.get("预期结果（JSON）", "{}")
        context_rule = step.get("上下文", "")
        
        step_result = {
            "step_index": step_index,
            "url": url,
            "success": True,
            "error": None
        }
        
        try:
            params = safe_parse_json(params_str, {})
            expected = safe_parse_json(expected_str, {})
            
            replaced_params = self.param_replacer.replace(params)
            step_result["request_params"] = replaced_params
            
            self.logger.info(f"步骤{step_index}: 调用接口 {url}")
            self.logger.info(f"请求参数: {json.dumps(replaced_params, ensure_ascii=False)}")
            
            response = self._send_request(url, replaced_params)
            step_result["response"] = response
            
            self.logger.info(f"响应结果: {json.dumps(response, ensure_ascii=False)}")
            
            if expected:
                try:
                    # assert_json_equals(response, expected)
                    assert response.get("status") == 1

                    self.logger.info(f"响应验证通过")
                except AssertionError as e:
                    step_result["success"] = False
                    step_result["error"] = f"响应验证失败: {str(e)}"
                    self.logger.error(f"响应验证失败: {e}")
                    return step_result
            
            if context_rule:
                context_data = self.response_extractor.extract_multiple(
                    response, 
                    [context_rule]
                )
                for key, value in context_data.items():
                    self.context.set(key, value)
                    self.logger.info(f"上下文提取: {key} = {value}")
                step_result["context_extracted"] = context_data
        
        except Exception as e:
            step_result["success"] = False
            step_result["error"] = str(e)
            self.logger.error(f"步骤{step_index}执行异常: {e}")
        
        return step_result
    
    def _send_request(self, url: str, params: Dict) -> Dict:
        if not url:
            return {"error": "接口地址为空"}
        
        try:
            if url.startswith("GET:"):
                endpoint = url[4:].strip()
                response = self.base_api.get(endpoint, params=params)
            elif url.startswith("POST:"):
                endpoint = url[5:].strip()
                response = self.base_api.post(endpoint, json=params)
            elif url.startswith("PUT:"):
                endpoint = url[4:].strip()
                response = self.base_api.put(endpoint, json=params)
            elif url.startswith("DELETE:"):
                endpoint = url[7:].strip()
                response = self.base_api.delete(endpoint)
            else:
                response = self.base_api.post(url, json=params)
            
            if hasattr(response, 'json'):
                return response.json()
            return response
        
        except Exception as e:
            self.logger.error(f"接口调用失败: {url}, 错误: {e}")
            return {"error": str(e)}
    
    def get_context(self) -> Dict:
        return self.context.get_all()