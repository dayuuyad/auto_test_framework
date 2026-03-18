from .base_api import BaseAPI
from typing import Dict, Optional, Any

class UserAPI(BaseAPI):
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(base_url, headers)
    
    def register(self, user_data: Dict[str, Any]) -> Any:
        endpoint = "/api/users/register"
        response = self.post(endpoint, json=user_data)
        return response.json()
    
    def login(self, credentials: Dict[str, str]) -> Any:
        endpoint = "/api/users/login"
        response = self.post(endpoint, json=credentials)
        return response.json()
    
    def get_user_info(self, user_id: int) -> Any:
        endpoint = f"/api/users/{user_id}"
        response = self.get(endpoint)
        return response.json()
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Any:
        endpoint = f"/api/users/{user_id}"
        response = self.put(endpoint, json=user_data)
        return response.json()
    
    def delete_user(self, user_id: int) -> Any:
        endpoint = f"/api/users/{user_id}"
        response = self.delete(endpoint)
        return response.json()