import pytest
from django.utils.html import json_script
from django.utils.safestring import SafeString


def test_json_script():
    value = {'key': 'value', 'array': [1, 2, 3]}
    element_id = 'test-element'
    
    # Call the function with the test data
    result = json_script(value, element_id)
    
    # Ensure the output is formatted as expected
    expected_json = '{"key": "value", "array": [1, 2, 3]}'
    expected_result = (
        '<script id="test-element" type="application/json">'
        + SafeString(expected_json).__str__()
        + '</script>'
    )
    
    assert result == expected_result


def test_json_script_with_special_characters():
    value = {'key': '<script>alert("xss")</script>', 'array': ['value1', 'value2']}
    element_id = 'special-char-element'

    # Call the function with special characters
    result = json_script(value, element_id)

    # Ensure the JSON is escaped correctly
    expected_json = '{"key": "\\u003cscript\\u003ealert(\\"xss\\")\\u003c/script\\u003e", "array": ["value1", "value2"]}'
    expected_result = (
        '<script id="special-char-element" type="application/json">'
        + SafeString(expected_json).__str__()
        + '</script>'
    )
    
    assert result == expected_result


def test_json_script_empty_value():
    value = {}
    element_id = 'empty-element'
    
    # Call the function with an empty dictionary
    result = json_script(value, element_id)

    # Ensure the output for empty value is correct
    expected_json = '{}'
    expected_result = (
        '<script id="empty-element" type="application/json">'
        + SafeString(expected_json).__str__()
        + '</script>'
    )
    
    assert result == expected_result