import json
import pytest
from django.utils.html import json_script

def test_json_script():
    # Test case 1: Simple dictionary
    value = {'key': 'value'}
    element_id = 'test-id-1'
    result = json_script(value, element_id)
    expected_json = json.dumps(value)
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    assert result == expected_result

    # Test case 2: Nested dictionary
    value = {'parent': {'child': 'value'}}
    element_id = 'test-id-2'
    result = json_script(value, element_id)
    expected_json = json.dumps(value)
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    assert result == expected_result

    # Test case 3: List of values
    value = ['value1', 'value2']
    element_id = 'test-id-3'
    result = json_script(value, element_id)
    expected_json = json.dumps(value)
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    assert result == expected_result

    # Test case 4: Empty value
    value = {}
    element_id = 'test-id-4'
    result = json_script(value, element_id)
    expected_json = json.dumps(value)
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    assert result == expected_result

    # Test case 5: Special characters
    value = {'key': '<script>alert("xss")</script>&'}
    element_id = 'test-id-5'
    result = json_script(value, element_id)
    expected_json = json.dumps(value)
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    assert result == expected_result