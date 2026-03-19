import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.json_assertion import (
    JSONAssertion,
    AssertionResult,
    assert_json,
    assert_json_equals,
    Matcher,
    MatcherRegistry
)


class TestAssertionResult:
    def test_success_result(self):
        result = AssertionResult(True, "测试通过")
        assert result.success is True
        assert "PASS" in str(result)
    
    def test_failure_result(self):
        result = AssertionResult(False, "测试失败", path="$.data", expected="a", actual="b")
        assert result.success is False
        assert "FAIL" in str(result)
        assert "$.data" in str(result)


class TestMatcherRegistry:
    def test_builtin_matchers(self):
        registry = MatcherRegistry()
        assert registry.has_matcher("notnull")
        assert registry.has_matcher("ignore")
        assert registry.has_matcher("isPhone")
        assert registry.has_matcher("isEmail")
    
    def test_register_custom_matcher(self):
        registry = MatcherRegistry()
        
        def custom_matcher(actual):
            return actual == "test", f"值是{actual}"
        
        registry.register("custom", custom_matcher)
        assert registry.has_matcher("custom")
        
        matcher = registry.get("custom")
        success, msg = matcher.match("test")
        assert success is True
    
    def test_matcher_case_insensitive(self):
        registry = MatcherRegistry()
        assert registry.has_matcher("NOTNULL")
        assert registry.has_matcher("Notnull")


class TestBuiltinMatchers:
    def test_notnull_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${notnull}", "value")
        assert result.success is True
        
        result = assertion.assert_json("${notnull}", None)
        assert result.success is False
        
        result = assertion.assert_json("${notnull}", "")
        assert result.success is False
        
        result = assertion.assert_json("${notnull}", [])
        assert result.success is False
    
    def test_ignore_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${ignore}", "any value")
        assert result.success is True
        
        result = assertion.assert_json("${ignore}", None)
        assert result.success is True
        
        result = assertion.assert_json("${ignore}", 123)
        assert result.success is True
    
    def test_phone_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isPhone}", "13812345678")
        assert result.success is True
        
        result = assertion.assert_json("${isPhone}", "12812345678")
        assert result.success is False
        
        result = assertion.assert_json("${isPhone}", "12345")
        assert result.success is False
        
        result = assertion.assert_json("${isPhone}", 12345678901)
        assert result.success is False
    
    def test_email_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isEmail}", "test@example.com")
        assert result.success is True
        
        result = assertion.assert_json("${isEmail}", "invalid-email")
        assert result.success is False
    
    def test_number_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isNumber}", 123)
        assert result.success is True
        
        result = assertion.assert_json("${isNumber}", 123.45)
        assert result.success is True
        
        result = assertion.assert_json("${isNumber}", "123")
        assert result.success is False
    
    def test_string_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isString}", "hello")
        assert result.success is True
        
        result = assertion.assert_json("${isString}", 123)
        assert result.success is False
    
    def test_boolean_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isBoolean}", True)
        assert result.success is True
        
        result = assertion.assert_json("${isBoolean}", False)
        assert result.success is True
        
        result = assertion.assert_json("${isBoolean}", "true")
        assert result.success is False
    
    def test_array_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isArray}", [1, 2, 3])
        assert result.success is True
        
        result = assertion.assert_json("${isArray}", "not array")
        assert result.success is False
    
    def test_object_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${isObject}", {"key": "value"})
        assert result.success is True
        
        result = assertion.assert_json("${isObject}", "not object")
        assert result.success is False
    
    def test_regex_matcher(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json("${regex:^\\d{4}$}", "1234")
        assert result.success is True
        
        result = assertion.assert_json("${regex:^\\d{4}$}", "123")
        assert result.success is False


class TestJSONAssertion:
    def test_primitive_comparison(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json(1, 1)
        assert result.success is True
        
        result = assertion.assert_json("hello", "hello")
        assert result.success is True
        
        result = assertion.assert_json(True, True)
        assert result.success is True
        
        result = assertion.assert_json(1, 2)
        assert result.success is False
    
    def test_dict_comparison(self):
        assertion = JSONAssertion()
        
        expected = {"name": "test", "value": 123}
        actual = {"name": "test", "value": 123}
        result = assertion.assert_json(expected, actual)
        assert result.success is True
        
        actual = {"name": "test", "value": 456}
        result = assertion.assert_json(expected, actual)
        assert result.success is False
    
    def test_nested_dict_comparison(self):
        assertion = JSONAssertion()
        
        expected = {
            "data": {
                "userId": "${notnull}",
                "name": "test"
            }
        }
        actual = {
            "data": {
                "userId": "L021U4DTPZKBI1P",
                "name": "test"
            }
        }
        result = assertion.assert_json(expected, actual)
        assert result.success is True
    
    def test_missing_field(self):
        assertion = JSONAssertion()
        
        expected = {"name": "test", "value": 123}
        actual = {"name": "test"}
        result = assertion.assert_json(expected, actual)
        assert result.success is False
        assert "缺少字段" in result.message
    
    def test_extra_field(self):
        assertion = JSONAssertion()
        
        expected = {"name": "test"}
        actual = {"name": "test", "extra": "value"}
        result = assertion.assert_json(expected, actual)
        assert result.success is False
        assert "多余字段" in result.message
    
    def test_list_comparison_ordered(self):
        assertion = JSONAssertion(ignore_array_order=False)
        
        expected = [1, 2, 3]
        actual = [1, 2, 3]
        result = assertion.assert_json(expected, actual)
        assert result.success is True
        
        actual = [3, 2, 1]
        result = assertion.assert_json(expected, actual)
        assert result.success is False
    
    def test_list_comparison_unordered(self):
        assertion = JSONAssertion(ignore_array_order=True)
        
        expected = [1, 2, 3]
        actual = [3, 2, 1]
        result = assertion.assert_json(expected, actual)
        assert result.success is True
    
    def test_list_with_objects_unordered(self):
        assertion = JSONAssertion(ignore_array_order=True)
        
        expected = [
            {"id": 1, "name": "a"},
            {"id": 2, "name": "b"}
        ]
        actual = [
            {"id": 2, "name": "b"},
            {"id": 1, "name": "a"}
        ]
        result = assertion.assert_json(expected, actual)
        assert result.success is True
    
    def test_list_length_mismatch(self):
        assertion = JSONAssertion()
        
        expected = [1, 2, 3]
        actual = [1, 2]
        result = assertion.assert_json(expected, actual)
        assert result.success is False
        assert "长度" in result.message
    
    def test_type_mismatch(self):
        assertion = JSONAssertion()
        
        result = assertion.assert_json({"a": 1}, [1, 2])
        assert result.success is False
        
        result = assertion.assert_json([1, 2], "string")
        assert result.success is False


class TestConvenienceFunctions:
    def test_assert_json_function(self):
        result = assert_json({"a": 1}, {"a": 1})
        assert result.success is True
    
    def test_assert_json_equals_success(self):
        assert_json_equals({"a": 1}, {"a": 1})
    
    def test_assert_json_equals_failure(self):
        with pytest.raises(AssertionError):
            assert_json_equals({"a": 1}, {"a": 2})
    
    def test_assert_json_with_ignore_array_order(self):
        result = assert_json([1, 2, 3], [3, 2, 1], ignore_array_order=True)
        assert result.success is True


class TestCustomMatcher:
    def test_custom_matcher_registration(self):
        assertion = JSONAssertion()
        
        def my_matcher(actual):
            if actual == "special":
                return True, "匹配成功"
            return False, f"期望special，实际为{actual}"
        
        assertion.register_matcher("myMatcher", my_matcher)
        
        result = assertion.assert_json("${myMatcher}", "special")
        assert result.success is True
        
        result = assertion.assert_json("${myMatcher}", "other")
        assert result.success is False


class TestRealWorldScenario:
    def test_api_response_assertion(self):
        expected = {
            "number": "1",
            "code": 0,
            "status": 1,
            "data": {
                "userId": "${notnull}"
            },
            "message": "请求成功",
            "ok": True,
            "msg": "请求成功"
        }
        
        actual = {
            "number": "1",
            "code": 0,
            "status": 1,
            "data": {
                "userId": "L021U4DTPZKBI1P"
            },
            "message": "请求成功",
            "ok": True,
            "msg": "请求成功"
        }
        
        result = assert_json(expected, actual)
        assert result.success is True
    
    def test_complex_nested_assertion(self):
        expected = {
            "code": 0,
            "data": {
                "user": {
                    "id": "${notnull}",
                    "phone": "${isPhone}",
                    "email": "${isEmail}",
                    "age": "${isNumber}"
                },
                "tags": "${ignore}"
            },
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"}
            ]
        }
        
        actual = {
            "code": 0,
            "data": {
                "user": {
                    "id": "user123",
                    "phone": "13800138000",
                    "email": "test@example.com",
                    "age": 25
                },
                "tags": ["tag1", "tag2", "tag3"]
            },
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"}
            ]
        }
        
        result = assert_json(expected, actual)
        assert result.success is True
    
    def test_unordered_array_in_response(self):
        expected = {
            "users": [
                {"id": 1},
                {"id": 2},
                {"id": 3}
            ]
        }
        
        actual = {
            "users": [
                {"id": 3},
                {"id": 1},
                {"id": 2}
            ]
        }
        
        result = assert_json(expected, actual, ignore_array_order=True)
        assert result.success is True
