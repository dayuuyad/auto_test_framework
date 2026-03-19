import sys
sys.path.insert(0, r'd:\traecode\test\src')
from utils.json_assertion import JSONAssertion, assert_json, assert_json_equals

# Test 1: Basic placeholder tests
print('=== Test 1: Placeholder tests ===')
assertion = JSONAssertion()

# notnull
result = assertion.assert_json('${notnull}', 'value')
assert result.success, f'notnull test failed: {result}'
print('PASS: notnull with value')

result = assertion.assert_json('${notnull}', None)
assert not result.success
print('PASS: notnull with None fails')

# ignore
result = assertion.assert_json('${ignore}', 'anything')
assert result.success
print('PASS: ignore matcher')

# phone
result = assertion.assert_json('${isPhone}', '13812345678')
assert result.success
print('PASS: valid phone')

result = assertion.assert_json('${isPhone}', '12345')
assert not result.success
print('PASS: invalid phone fails')

# email
result = assertion.assert_json('${isEmail}', 'test@example.com')
assert result.success
print('PASS: valid email')

# regex
result = assertion.assert_json('${regex:^\\d{4}$}', '1234')
assert result.success
print('PASS: regex match')

# Test 2: Dict comparison
print('\n=== Test 2: Dict comparison ===')
expected = {'name': 'test', 'value': 123}
actual = {'name': 'test', 'value': 123}
result = assertion.assert_json(expected, actual)
assert result.success
print('PASS: dict equal')

# Test 3: Nested dict with placeholders
print('\n=== Test 3: Nested dict with placeholders ===')
expected = {
    'data': {
        'userId': '${notnull}',
        'name': 'test'
    }
}
actual = {
    'data': {
        'userId': 'L021U4DTPZKBI1P',
        'name': 'test'
    }
}
result = assertion.assert_json(expected, actual)
assert result.success, f'Nested dict test failed: {result}'
print('PASS: nested dict with notnull')

# Test 4: Array order
print('\n=== Test 4: Array order ===')
assertion_ordered = JSONAssertion(ignore_array_order=False)
result = assertion_ordered.assert_json([1, 2, 3], [3, 2, 1])
assert not result.success
print('PASS: ordered array mismatch detected')

assertion_unordered = JSONAssertion(ignore_array_order=True)
result = assertion_unordered.assert_json([1, 2, 3], [3, 2, 1])
assert result.success
print('PASS: unordered array match')

# Test 5: Real world scenario
print('\n=== Test 5: Real world scenario ===')
expected = {
    'number': '1',
    'code': 0,
    'status': 1,
    'data': {
        'userId': '${notnull}'
    },
    'message': '请求成功',
    'ok': True,
    'msg': '请求成功'
}
actual = {
    'number': '1',
    'code': 0,
    'status': 1,
    'data': {
        'userId': 'L021U4DTPZKBI1P'
    },
    'message': '请求成功',
    'ok': True,
    'msg': '请求成功'
}
result = assert_json(expected, actual)
assert result.success, f'Real world test failed: {result}'
print('PASS: real world API response')

# Test 6: Custom matcher
print('\n=== Test 6: Custom matcher ===')
def my_matcher(actual):
    if actual == 'special':
        return True, '匹配成功'
    return False, f'期望special，实际为{actual}'

assertion.register_matcher('myMatcher', my_matcher)
result = assertion.assert_json('${myMatcher}', 'special')
assert result.success
print('PASS: custom matcher')

# Test 7: assert_json_equals
print('\n=== Test 7: assert_json_equals ===')
assert_json_equals({'a': 1}, {'a': 1})
print('PASS: assert_json_equals success')

try:
    assert_json_equals({'a': 1}, {'a': 2})
    assert False, 'Should have raised'
except AssertionError:
    print('PASS: assert_json_equals raises on mismatch')

print('\n=== All tests passed! ===')
