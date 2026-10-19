import pytest
from django.utils.html import json_script
from django.utils.encoding import force_str
from django.core.serializers.json import DjangoJSONEncoder

def test_json_script_valid_input():
    value = {'name': 'John', 'age': 30}
    element_id = 'user-data'
    result = json_script(value, element_id)
    
    expected_json = '{"name": "John", "age": 30}'
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    
    assert result == expected_result

def test_json_script_empty_dict():
    value = {}
    element_id = 'empty-data'
    result = json_script(value, element_id)
    
    expected_json = '{}'
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    
    assert result == expected_result

def test_json_script_special_characters():
    value = {'html': '<div>Test & "Quotes"</div>', 'boolean': True}
    element_id = 'special-chars'
    result = json_script(value, element_id)
    
    expected_json = '{"html": "<div>Test & \\"Quotes\\"</div>", "boolean": true}'
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    
    assert result == expected_result

def test_json_script_with_unicode():
    value = {'message': 'Hello 😊'}
    element_id = 'unicode-message'
    result = json_script(value, element_id)
    
    expected_json = '{"message": "Hello \ud83d\ude0a"}'
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    
    assert result == expected_result

def test_json_script_invalid_id():
    value = {'data': 123}
    element_id = 'invalid-id<>'
    result = json_script(value, element_id)
    
    expected_json = '{"data": 123}'
    expected_result = f'<script id="{element_id}" type="application/json">{expected_json}</script>'
    
    assert result == expected_result