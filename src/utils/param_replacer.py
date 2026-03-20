import re
from typing import Any, Dict, List, Union
from utils.context_manager import ContextManager


class ParamReplacer:
    PLACEHOLDER_PATTERN = re.compile(r'\$\{([^}]+)\}')
    
    def __init__(self, context: ContextManager):
        self.context = context
    
    def replace(self, data: Any) -> Any:
        if isinstance(data, str):
            return self._replace_string(data)
        elif isinstance(data, dict):
            return self._replace_dict(data)
        elif isinstance(data, list):
            return self._replace_list(data)
        else:
            return data
    
    def _replace_string(self, text: str) -> Any:
        placeholders = self.extract_placeholders(text)
        
        if not placeholders:
            return text
        
        if text.startswith('${') and text.endswith('}'):
            placeholder = text[2:-1]
            value = self.context.get(placeholder)
            if value is not None:
                return value
            return text
        
        result = text
        for placeholder in placeholders:
            value = self.context.get(placeholder)
            if value is not None:
                result = result.replace(f'${{{placeholder}}}', str(value))
        
        return result
    
    def _replace_dict(self, data: Dict) -> Dict:
        result = {}
        for key, value in data.items():
            new_key = self._replace_string(key)
            new_value = self.replace(value)
            result[new_key] = new_value
        return result
    
    def _replace_list(self, data: List) -> List:
        return [self.replace(item) for item in data]
    
    def extract_placeholders(self, text: str) -> List[str]:
        if not isinstance(text, str):
            return []
        return self.PLACEHOLDER_PATTERN.findall(text)
    
    def has_placeholders(self, text: str) -> bool:
        if not isinstance(text, str):
            return False
        return bool(self.PLACEHOLDER_PATTERN.search(text))