import json
import os
from datetime import datetime, timedelta
from typing import Optional, List


class AuthManager:
    def __init__(self, config):
        self.config = config
        self.cookies_file = config.COOKIES_FILE
        self.cookie_expire_hours = getattr(config, 'COOKIE_EXPIRE_HOURS', 24)
    
    def load_cookies(self) -> Optional[List[dict]]:
        if not os.path.exists(self.cookies_file):
            return None
        
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            expire_time = datetime.fromisoformat(data.get('expire_time', ''))
            if expire_time > datetime.now():
                return data.get('cookies', [])
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
        
        return None
    
    def save_cookies(self, cookies: List[dict]) -> None:
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
        
        data = {
            'cookies': cookies,
            'expire_time': (datetime.now() + timedelta(hours=self.cookie_expire_hours)).isoformat()
        }
        
        with open(self.cookies_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_cookies(self) -> None:
        if os.path.exists(self.cookies_file):
            os.remove(self.cookies_file)
    
    def is_cookies_valid(self) -> bool:
        return self.load_cookies() is not None
