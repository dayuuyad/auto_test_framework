import redis
from typing import Optional, Any

class RedisClient:
    def __init__(self, host: str, port: int, password: Optional[str] = None, db: int = 0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.client = None
    
    def connect(self) -> None:
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[str]:
        return self.client.get(key)
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        return self.client.set(key, value, ex=ex)
    
    def delete(self, key: str) -> int:
        return self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0
    
    def close(self) -> None:
        if self.client:
            self.client.close()