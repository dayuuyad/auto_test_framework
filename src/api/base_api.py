import requests
import json
from typing import Dict, Optional, Any, Union

class BaseAPI:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """GET请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        response = self.session.get(url, params=params, **kwargs)
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """POST请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        response = self.session.post(url, data=data, json=json, **kwargs)
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """PUT请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        response = self.session.put(url, data=data, json=json, **kwargs)
        return self._handle_response(response)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """DELETE请求，自动处理URL格式化和错误检查"""
        url = self._build_url(endpoint)
        response = self.session.delete(url, **kwargs)
        return self._handle_response(response)
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
        self.session.headers.update(headers)
    
    def get_headers(self) -> Dict[str, str]:
        return dict(self.session.headers)
    
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