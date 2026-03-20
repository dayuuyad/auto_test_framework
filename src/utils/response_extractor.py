import re
from typing import Any, Dict, List, Tuple, Union
from utils.logger import global_logger


class ResponseExtractor:
    ARRAY_INDEX_PATTERN = re.compile(r'(\w+)\[(\d+)\]')
    
    def __init__(self):
        self.logger = global_logger
    
    def extract(self, response: Dict, path: str) -> Any:
        if not path or not response:
            return None
        
        try:
            parts = self._parse_path(path)
            current = response
            
            for part in parts:
                if current is None:
                    return None
                
                array_match = self.ARRAY_INDEX_PATTERN.match(part)
                if array_match:
                    key = array_match.group(1)
                    index = int(array_match.group(2))
                    
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                        if isinstance(current, list) and 0 <= index < len(current):
                            current = current[index]
                        else:
                            return None
                    else:
                        return None
                else:
                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        return None
            
            return current
        except Exception as e:
            self.logger.error(f"提取响应路径失败: {path}, 错误: {e}")
            return None
    
    def _parse_path(self, path: str) -> List[str]:
        return path.split('.')
    
    def parse_extraction_rule(self, rule: str) -> Tuple[str, str]:
        if not rule or ':' not in rule:
            return None, None
        
        parts = rule.split(':', 1)
        if len(parts) != 2:
            return None, None
        
        context_name = parts[0].strip()
        path = parts[1].strip()
        
        return context_name, path
    
    def extract_multiple(self, response: Dict, rules: List[str]) -> Dict[str, Any]:
        result = {}
        
        for rule in rules:
            if not rule:
                continue
            
            context_name, path = self.parse_extraction_rule(rule)
            if context_name and path:
                value = self.extract(response, path)
                if value is not None:
                    result[context_name] = value
                    self.logger.info(f"提取上下文: {context_name} = {value}")
        
        return result