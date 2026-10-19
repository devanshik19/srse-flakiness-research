import json
import pytest
from django.utils.html import json_script
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

def test_json_script():
    # Test with a simple dictionary
    data = {"name": "John", "age": 30}
    element_id = "user-data"
    expected_json = json.dumps(data, cls=DjangoJSONEncoder)
    expected_output = f'<script id="{element_id}" type="application/json">{mark_safe(expected_json)}</script>'
    
    output = json_script(data, element_id)
    assert output == expected_output

    # Test with a list
    data = [1, 2, 3, 4, 5]
    element_id = "number-data"
    expected_json = json.dumps(data, cls=DjangoJSONEncoder)
    expected_output = f'<script id="{element_id}" type="application/json">{mark_safe(expected_json)}</script>'
    
    output = json_script(data, element_id)
    assert output == expected_output

    # Test with a nested structure
    data = {"items": [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]}
    element_id = "nested-data"
    expected_json = json.dumps(data, cls=DjangoJSONEncoder)
    expected_output = f'<script id="{element_id}" type="application/json">{mark_safe(expected_json)}</script>'
    
    output = json_script(data, element_id)
    assert output == expected_output

    # Test with special characters
    data = {"key": "<script>alert('test')</script>"}
    element_id = "special-char-data"
    expected_json = json.dumps(data, cls=DjangoJSONEncoder)
    expected_output = f'<script id="{element_id}" type="application/json">{mark_safe(expected_json)}</script>'
    
    output = json_script(data, element_id)
    assert output == expected_output