import pytest
from django.utils.html import json_script
from django.core.serializers.json import DjangoJSONEncoder

def test_json_script():
    # Test case 1: Basic dictionary
    value = {'key': 'value'}
    element_id = 'test-id-1'
    expected_output = (
        '<script id="test-id-1" type="application/json">{}</script>'
    ).format('{"key": "value"}')
    assert json_script(value, element_id) == expected_output

    # Test case 2: List with mixed data types
    value = [1, 2, 3, {'key': 'value'}, True, None]
    element_id = 'test-id-2'
    expected_output = (
        '<script id="test-id-2" type="application/json">{}</script>'
    ).format('[1, 2, 3, {"key": "value"}, true, null]')
    assert json_script(value, element_id) == expected_output

    # Test case 3: Nested dictionary
    value = {'outer_key': {'inner_key': 'inner_value'}}
    element_id = 'test-id-3'
    expected_output = (
        '<script id="test-id-3" type="application/json">{}</script>'
    ).format('{"outer_key": {"inner_key": "inner_value"}}')
    assert json_script(value, element_id) == expected_output

    # Test case 4: Special characters in keys and values
    value = {'key<>&"': 'value<>&"'}
    element_id = 'test-id-4'
    expected_output = (
        '<script id="test-id-4" type="application/json">{}</script>'
    ).format('{"key<>&\\"": "value<>&\\""}')
    assert json_script(value, element_id) == expected_output