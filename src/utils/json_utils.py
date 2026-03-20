import json
from typing import Any, Union

from utils.logger import global_logger


def safe_parse_json(
    value: Any, 
    default: Any = None, 
    strict: bool = False
) -> Union[dict, list, None]:
    """
    安全解析JSON字符串
    
    Args:
        value: 待解析的值（字符串、dict、list或其他）
        default: 解析失败时的默认返回值
        strict: 严格模式，解析结果必须为dict/list类型，否则返回default
    
    Returns:
        解析后的JSON对象或默认值
    """
    if value is None:
        return default
    
    if isinstance(value, (dict, list)):
        return value

    if not isinstance(value, str):
        return default
    
    if not value.strip():
        return default
    
    try:
        result = json.loads(value)
        if strict and not isinstance(result, (dict, list)):
            return default        
        return result
    except (json.JSONDecodeError, TypeError) as e:
        global_logger.error(f"JSON解析失败: {e}, 原始数据: {value}")
        return default
