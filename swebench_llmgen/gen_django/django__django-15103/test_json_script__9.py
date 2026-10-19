import pytest
from django.utils.html import json_script
from django.core.serializers.json import DjangoJSONEncoder

def test_json_script():
    value = {"key": "value", "number": 123, "list": [1, 2, 3]}
    element_id = "test-json-element"

    expected_output = f'<script id="{element_id}" type="application/json">{DjangoJSONEncoder().encode(value).translate(str.maketrans({"<": "\\u003C", ">": "\\u003E", "&": "\\u0026", "'": "\\u0027", '"': "\\u0022"}))}</script>'
    
    result = json_script(value, element_id)
    
    assert result == expected_output

def test_json_script_empty():
    value = {}
    element_id = "empty-json-element"

    expected_output = f'<script id="{element_id}" type="application/json">{DjangoJSONEncoder().encode(value).translate(str.maketrans({"<": "\\u003C", ">": "\\u003E", "&": "\\u0026", "'": "\\u0027", '"': "\\u0022"}))}</script>'
    
    result = json_script(value, element_id)

    assert result == expected_output

def test_json_script_special_characters():
    value = {"html": "<div>", "string": "&", "quote": "\""}
    element_id = "special-characters-element"

    expected_output = f'<script id="{element_id}" type="application/json">{DjangoJSONEncoder().encode(value).translate(str.maketrans({"<": "\\u003C", ">": "\\u003E", "&": "\\u0026", "'": "\\u0027", '"': "\\u0022"}))}</script>'
    
    result = json_script(value, element_id)
    
    assert result == expected_output