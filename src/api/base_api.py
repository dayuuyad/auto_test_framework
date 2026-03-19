import requests
import json
import hmac
import hashlib
import base64
from typing import Dict, Optional, Any, Union

class BaseAPI:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, 
                 secret_key: Optional[str] = None, signature_algorithm: str = "hmac-sha256"):
        self.base_url = base_url
        self.headers = headers or {}
        self.secret_key = secret_key
        self.signature_algorithm = signature_algorithm
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 用于存储请求和响应数据
        self._last_request_data = None
        self._last_response_data = None
    
    def _capture_request_data(self, method: str, url: str, **request_kwargs) -> None:
        """捕获请求数据"""
        # 获取请求级别的headers（从kwargs中）
        request_headers = request_kwargs.get('headers', {})
        # print(f"22222222222222222222222request_kwargs: {request_kwargs}")
        # print(f"request_headers: {request_headers}")

        # 合并session headers和请求级别headers
        merged_headers = {**dict[str, str | bytes](self.session.headers), **request_headers}
        # print(f"合并后的headers: {merged_headers}")
        self._last_request_data = {
            'method': method,
            'url': url,
            'headers': merged_headers,  # 记录完整的headers
            'session_headers': dict(self.session.headers),  # 单独记录session headers
            'request_headers': request_headers,  # 单独记录请求级别headers
            **{k: v for k, v in request_kwargs.items() if k != 'headers'}  # 排除headers，避免重复
        }
    
    def _capture_response_data(self, response: requests.Response) -> None:
        """捕获响应数据"""
        self._last_response_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.text,
            'json': self._safe_json_decode(response.text)
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """GET请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        
        # 捕获请求数据
        self._capture_request_data('GET', url, params=params, kwargs=kwargs)
        
        response = self.session.get(url, params=params, **kwargs)
        
        # 捕获响应数据
        self._capture_response_data(response)
        
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, 
             sign_body: bool = False, **kwargs) -> Dict[str, Any]:
        """POST请求，自动处理URL格式化和错误检查
        
        Args:
            endpoint: API端点
            data: 表单数据
            json: JSON数据
            sign_body: 是否对body进行签名
            **kwargs: 其他请求参数
            
        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        
        # 处理签名
        headers = kwargs.get('headers', {})
        # print(f"111111111111111111111111111POST请求头: {headers}")
        # print(f"kwargs: {kwargs}")

        if sign_body:
            # 优先使用json数据，如果没有则使用data
            sign_data = json if json is not None else data
            if sign_data is not None:
                headers = self._add_signature_to_headers(sign_data, headers)
                kwargs['headers'] = headers
        
        # print(f"11111111111111111111111111headers: {headers}")
        # 捕获请求数据
        self._capture_request_data('POST', url, data=data, json=json, headers=headers)
        
        response = self.session.post(url, data=data, json=json, **kwargs)
        
        # 捕获响应数据
        self._capture_response_data(response)
        
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """PUT请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        
        # 捕获请求数据
        self._capture_request_data('PUT', url, data=data, json=json, kwargs=kwargs)
        
        response = self.session.put(url, data=data, json=json, **kwargs)
        
        # 捕获响应数据
        self._capture_response_data(response)
        
        return self._handle_response(response)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """DELETE请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        
        # 捕获请求数据
        self._capture_request_data('DELETE', url, kwargs=kwargs)
        
        response = self.session.delete(url, **kwargs)
        
        # 捕获响应数据
        self._capture_response_data(response)
        
        return self._handle_response(response)
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
        self.session.headers.update(headers)
    
    def get_headers(self) -> Dict[str, str]:
        return dict(self.session.headers)
    
    def set_signature_config(self, secret_key: str, algorithm: str = "hmac-sha1") -> None:
        """设置签名配置"""
        self.secret_key = secret_key
        self.signature_algorithm = algorithm
    
    def _generate_signature(self, data: Union[str, Dict[str, Any]]) -> str:
        """生成body签名"""
        if not self.secret_key:
            raise ValueError("签名密钥未设置，请先调用set_signature_config方法")
        
        # 将数据转换为字符串
        if isinstance(data, dict):
            data_str = json.dumps(data, separators=(',', ':'), sort_keys=True)
        else:
            data_str = str(data)
        
        # 根据算法生成签名
        if self.signature_algorithm == "hmac-sha1":
            signature = hmac.new(
                self.secret_key.encode('utf-8'),
                data_str.encode('utf-8'),
                hashlib.sha1
            ).digest()
        elif self.signature_algorithm == "hmac-sha256":
            signature = hmac.new(
                self.secret_key.encode('utf-8'),
                data_str.encode('utf-8'),
                hashlib.sha256
            ).digest()
        elif self.signature_algorithm == "sha256":
            signature = hashlib.sha256(data_str.encode('utf-8')).digest()
        else:
            raise ValueError(f"不支持的签名算法: {self.signature_algorithm}")
        
        # 返回base64编码的签名
        return base64.b64encode(signature).decode('utf-8')
    
    def _add_signature_to_headers(self, data: Union[str, Dict[str, Any]], headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """添加签名到请求头"""
        if not self.secret_key:
            return headers or {}
        
        signature = self._generate_signature(data)
        # print(signature)
        headers = headers or {}
        headers['Content-Signature'] = "HMAC-SHA1 " + signature
        # print(headers)
        # headers['X-Signature'] = signature
        # headers['X-Signature-Algorithm'] = self.signature_algorithm
        
        return headers
    
    def close(self) -> None:
        self.session.close()
    
    def _build_url(self, endpoint: str) -> str:
        """构建完整的URL"""
        return f"{self.base_url}{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """统一处理响应，包括错误检查和JSON解析"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP错误 {response.status_code}: {response.text}") from e
        except requests.exceptions.JSONDecodeError as e:
            raise Exception(f"响应JSON解析失败: {response.text}") from e
    
    def _safe_json_decode(self, text: str) -> Optional[Dict[str, Any]]:
        """安全地解析JSON，如果解析失败返回None"""
        try:
            return json.loads(text) if text.strip() else None
        except (json.JSONDecodeError, ValueError):
            return None
    
    def get_last_request_data(self) -> Optional[Dict[str, Any]]:
        """获取最后一次请求的数据"""
        return self._last_request_data
    
    def get_last_response_data(self) -> Optional[Dict[str, Any]]:
        """获取最后一次响应的数据"""
        return self._last_response_data
    
    def clear_request_response_data(self) -> None:
        """清除存储的请求和响应数据"""
        self._last_request_data = None
        self._last_response_data = None