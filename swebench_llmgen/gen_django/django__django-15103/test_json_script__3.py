import pytest
from django.utils.html import json_script
from django.utils.safestring import mark_safe
import json

def test_json_script():
    # Test case 1: Basic dictionary
    value = {'key': 'value', 'int': 42, 'list': [1, 2, 3]}
    element_id = 'test_element'
    expected_output = (
        '<script id="test_element" type="application/json">{}</script>'
    ).format(mark_safe(json.dumps(value, cls=json.JSONEncoder)))
    assert json_script(value, element_id) == expected_output

    # Test case 2: List of values
    value = [1, 2, 3, "string"]
    element_id = 'test_list'
    expected_output = (
        '<script id="test_list" type="application/json">{}</script>'
    ).format(mark_safe(json.dumps(value, cls=json.JSONEncoder)))
    assert json_script(value, element_id) == expected_output

    # Test case 3: String with special characters
    value = '<script>alert("XSS")</script>'
    element_id = 'test_string'
    expected_output = (
        '<script id="test_string" type="application/json">{}</script>'
    ).format(mark_safe(json.dumps(value, cls=json.JSONEncoder)))
    assert json_script(value, element_id) == expected_output

    # Test case 4: Complex nested data
    value = {
        'user': {
            'name': 'John Doe',
            'admin': True,
            'roles': ['user', 'admin']
        }
    }
    element_id = 'test_complex'
    expected_output = (
        '<script id="test_complex" type="application/json">{}</script>'
    ).format(mark_safe(json.dumps(value, cls=json.JSONEncoder)))
    assert json_script(value, element_id) == expected_output