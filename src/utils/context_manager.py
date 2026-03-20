from typing import Any, Dict
import threading


class ContextManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._context = {}
                    cls._instance._context_lock = threading.Lock()
        return cls._instance
    
    def set(self, key: str, value: Any) -> None:
        with self._context_lock:
            self._context[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        with self._context_lock:
            return self._context.get(key, default)
    
    def contains(self, key: str) -> bool:
        with self._context_lock:
            return key in self._context
    
    def clear(self) -> None:
        with self._context_lock:
            self._context.clear()
    
    def get_all(self) -> Dict[str, Any]:
        with self._context_lock:
            return dict(self._context)
    
    def update(self, data: Dict[str, Any]) -> None:
        with self._context_lock:
            self._context.update(data)
    
    def remove(self, key: str) -> None:
        with self._context_lock:
            if key in self._context:
                del self._context[key]
    
    def __str__(self) -> str:
        return str(self.get_all())
    
    def __repr__(self) -> str:
        return f"ContextManager({self.get_all()})"