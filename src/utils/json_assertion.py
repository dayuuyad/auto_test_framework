import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


@dataclass
class AssertionResult:
    success: bool
    message: str
    path: str = ""
    expected: Any = None
    actual: Any = None
    errors: List['AssertionResult'] = field(default_factory=list)
    
    def __str__(self) -> str:
        if self.success:
            return f"[PASS] {self.message}"
        
        result = f"[FAIL] {self.message}"
        if self.path:
            result = f"[FAIL] Path: {self.path} - {self.message}"
        if self.expected is not None or self.actual is not None:
            result += f"\n  Expected: {self.expected}\n  Actual: {self.actual}"
        if self.errors:
            for err in self.errors:
                err_str = str(err)
                for line in err_str.split('\n'):
                    result += f"\n  {line}"
        return result


class Matcher:
    def __init__(self, name: str, match_func: Callable[[Any], Tuple[bool, str]]):
        self.name = name
        self._match_func = match_func
    
    def match(self, actual: Any) -> Tuple[bool, str]:
        return self._match_func(actual)


class MatcherRegistry:
    def __init__(self):
        self._matchers: Dict[str, Matcher] = {}
        self._register_builtin_matchers()
    
    def register(self, name: str, matcher: Union[Matcher, Callable[[Any], Tuple[bool, str]]]) -> None:
        if callable(matcher) and not isinstance(matcher, Matcher):
            matcher = Matcher(name, matcher)
        self._matchers[name.lower()] = matcher
    
    def get(self, name: str) -> Optional[Matcher]:
        return self._matchers.get(name.lower())
    
    def has_matcher(self, name: str) -> bool:
        return name.lower() in self._matchers
    
    def _register_builtin_matchers(self) -> None:
        self.register("notnull", self._notnull_matcher)
        self.register("ignore", self._ignore_matcher)
        self.register("isphone", self._phone_matcher)
        self.register("isemail", self._email_matcher)
        self.register("isnumber", self._number_matcher)
        self.register("isstring", self._string_matcher)
        self.register("isboolean", self._boolean_matcher)
        self.register("isarray", self._array_matcher)
        self.register("isobject", self._object_matcher)
    
    @staticmethod
    def _notnull_matcher(actual: Any) -> Tuple[bool, str]:
        if actual is None:
            return False, "值为None，期望非空"
        if isinstance(actual, str) and actual.strip() == "":
            return False, "值为空字符串，期望非空"
        if isinstance(actual, (list, dict)) and len(actual) == 0:
            return False, "值为空容器，期望非空"
        return True, "值非空"
    
    @staticmethod
    def _ignore_matcher(actual: Any) -> Tuple[bool, str]:
        return True, "字段已忽略"
    
    @staticmethod
    def _phone_matcher(actual: Any) -> Tuple[bool, str]:
        if not isinstance(actual, str):
            return False, f"手机号应为字符串，实际类型为{type(actual).__name__}"
        pattern = r'^1[3-9]\d{9}$'
        if re.match(pattern, actual):
            return True, "手机号格式正确"
        return False, f"'{actual}' 不是有效的手机号格式"
    
    @staticmethod
    def _email_matcher(actual: Any) -> Tuple[bool, str]:
        if not isinstance(actual, str):
            return False, f"邮箱应为字符串，实际类型为{type(actual).__name__}"
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, actual):
            return True, "邮箱格式正确"
        return False, f"'{actual}' 不是有效的邮箱格式"
    
    @staticmethod
    def _number_matcher(actual: Any) -> Tuple[bool, str]:
        if isinstance(actual, (int, float)) and not isinstance(actual, bool):
            return True, "数字类型正确"
        return False, f"期望数字类型，实际类型为{type(actual).__name__}"
    
    @staticmethod
    def _string_matcher(actual: Any) -> Tuple[bool, str]:
        if isinstance(actual, str):
            return True, "字符串类型正确"
        return False, f"期望字符串类型，实际类型为{type(actual).__name__}"
    
    @staticmethod
    def _boolean_matcher(actual: Any) -> Tuple[bool, str]:
        if isinstance(actual, bool):
            return True, "布尔类型正确"
        return False, f"期望布尔类型，实际类型为{type(actual).__name__}"
    
    @staticmethod
    def _array_matcher(actual: Any) -> Tuple[bool, str]:
        if isinstance(actual, list):
            return True, "数组类型正确"
        return False, f"期望数组类型，实际类型为{type(actual).__name__}"
    
    @staticmethod
    def _object_matcher(actual: Any) -> Tuple[bool, str]:
        if isinstance(actual, dict):
            return True, "对象类型正确"
        return False, f"期望对象类型，实际类型为{type(actual).__name__}"


class JSONAssertion:
    PLACEHOLDER_PATTERN = re.compile(r'^\$\{(.+)\}$')
    
    def __init__(self, ignore_array_order: bool = False):
        self._ignore_array_order = ignore_array_order
        self._registry = MatcherRegistry()
    
    def register_matcher(self, name: str, matcher: Union[Matcher, Callable[[Any], Tuple[bool, str]]]) -> None:
        self._registry.register(name, matcher)
    
    def assert_json(self, expected: Any, actual: Any, path: str = "$") -> AssertionResult:
        if expected is None and actual is None:
            return AssertionResult(True, "两者都为None", path, expected, actual)
        
        if isinstance(expected, str):
            match = self.PLACEHOLDER_PATTERN.match(expected)
            if match:
                matcher_name = match.group(1)
                return self._handle_placeholder(matcher_name, actual, path, expected)
        
        if isinstance(expected, dict):
            return self._compare_dict(expected, actual, path)
        
        if isinstance(expected, list):
            return self._compare_list(expected, actual, path)
        
        return self._compare_primitive(expected, actual, path)
    
    def _handle_placeholder(self, matcher_name: str, actual: Any, path: str, expected: Any) -> AssertionResult:
        if matcher_name.lower().startswith("regex:"):
            pattern = matcher_name[6:]
            return self._handle_regex(pattern, actual, path, expected)
        
        matcher = self._registry.get(matcher_name)
        if matcher is None:
            return AssertionResult(
                False, 
                f"未知的匹配器: {matcher_name}", 
                path, 
                expected, 
                actual
            )
        
        success, message = matcher.match(actual)
        return AssertionResult(success, message, path, expected, actual)
    
    def _handle_regex(self, pattern: str, actual: Any, path: str, expected: Any) -> AssertionResult:
        if not isinstance(actual, str):
            return AssertionResult(
                False, 
                f"正则匹配需要字符串，实际类型为{type(actual).__name__}", 
                path, 
                expected, 
                actual
            )
        
        try:
            if re.match(pattern, actual):
                return AssertionResult(True, f"正则匹配成功: {pattern}", path, expected, actual)
            return AssertionResult(False, f"'{actual}' 不匹配正则: {pattern}", path, expected, actual)
        except re.error as e:
            return AssertionResult(False, f"无效的正则表达式: {pattern}, 错误: {e}", path, expected, actual)
    
    def _compare_dict(self, expected: Dict, actual: Any, path: str) -> AssertionResult:
        if not isinstance(actual, dict):
            return AssertionResult(
                False, 
                f"期望字典，实际类型为{type(actual).__name__}", 
                path, 
                expected, 
                actual
            )
        
        errors: List[AssertionResult] = []
        
        for key in expected:
            if key not in actual:
                if isinstance(expected[key], str) and self.PLACEHOLDER_PATTERN.match(expected[key]):
                    matcher_name = self.PLACEHOLDER_PATTERN.match(expected[key]).group(1)
                    if matcher_name.lower() == "ignore":
                        continue
                
                errors.append(AssertionResult(
                    False, 
                    f"缺少字段: {key}", 
                    f"{path}.{key}", 
                    expected[key], 
                    None
                ))
        
        for key in actual:
            if key not in expected:
                errors.append(AssertionResult(
                    False, 
                    f"多余字段: {key}", 
                    f"{path}.{key}", 
                    None, 
                    actual[key]
                ))
        
        for key in expected:
            if key in actual:
                result = self.assert_json(expected[key], actual[key], f"{path}.{key}")
                if not result.success:
                    errors.append(result)
        
        if errors:
            return AssertionResult(False, "字典比较失败", path, expected, actual, errors)
        return AssertionResult(True, "字典比较成功", path, expected, actual)
    
    def _compare_list(self, expected: List, actual: Any, path: str) -> AssertionResult:
        if not isinstance(actual, list):
            return AssertionResult(
                False, 
                f"期望列表，实际类型为{type(actual).__name__}", 
                path, 
                expected, 
                actual
            )
        
        if len(expected) != len(actual):
            return AssertionResult(
                False, 
                f"列表长度不匹配，期望{len(expected)}，实际{len(actual)}", 
                path, 
                expected, 
                actual
            )
        
        if self._ignore_array_order:
            return self._compare_list_unordered(expected, actual, path)
        
        return self._compare_list_ordered(expected, actual, path)
    
    def _compare_list_ordered(self, expected: List, actual: List, path: str) -> AssertionResult:
        errors: List[AssertionResult] = []
        
        for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
            result = self.assert_json(exp_item, act_item, f"{path}[{i}]")
            if not result.success:
                errors.append(result)
        
        if errors:
            return AssertionResult(False, "有序列表比较失败", path, expected, actual, errors)
        return AssertionResult(True, "有序列表比较成功", path, expected, actual)
    
    def _compare_list_unordered(self, expected: List, actual: List, path: str) -> AssertionResult:
        errors: List[AssertionResult] = []
        matched_indices: set = set()
        
        for i, exp_item in enumerate(expected):
            found_match = False
            for j, act_item in enumerate(actual):
                if j in matched_indices:
                    continue
                
                result = self.assert_json(exp_item, act_item, f"{path}[{i}]")
                if result.success:
                    matched_indices.add(j)
                    found_match = True
                    break
            
            if not found_match:
                errors.append(AssertionResult(
                    False, 
                    f"未找到匹配元素", 
                    f"{path}[{i}]", 
                    exp_item, 
                    None
                ))
        
        if errors:
            return AssertionResult(False, "无序列表比较失败", path, expected, actual, errors)
        return AssertionResult(True, "无序列表比较成功", path, expected, actual)
    
    def _compare_primitive(self, expected: Any, actual: Any, path: str) -> AssertionResult:
        if expected == actual:
            return AssertionResult(True, "值相等", path, expected, actual)
        
        if isinstance(expected, float) and isinstance(actual, float):
            if abs(expected - actual) < 1e-9:
                return AssertionResult(True, "浮点数近似相等", path, expected, actual)
        
        return AssertionResult(
            False, 
            f"值不匹配: 期望 {expected!r}，实际 {actual!r}", 
            path, 
            expected, 
            actual
        )


def assert_json(
    expected: Any, 
    actual: Any, 
    ignore_array_order: bool = False,
    path: str = "$"
) -> AssertionResult:
    assertion = JSONAssertion(ignore_array_order=ignore_array_order)
    return assertion.assert_json(expected, actual, path)


def assert_json_equals(
    expected: Any, 
    actual: Any, 
    ignore_array_order: bool = False,
    path: str = "$"
) -> None:
    result = assert_json(expected, actual, ignore_array_order, path)
    if not result.success:
        raise AssertionError(str(result))
