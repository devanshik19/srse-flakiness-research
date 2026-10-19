import pytest
from django.utils.html import json_script
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import format_html, mark_safe

def test_json_script():
    # Test case 1: Simple dictionary
    value = {'key': 'value', 'num': 123}
    element_id = 'test-id-1'
    expected_output = format_html('<script id="{}" type="application/json">{{"key": "value", "num": 123}}</script>', element_id)
    assert json_script(value, element_id) == expected_output

    # Test case 2: List with mixed types
    value = [1, 2, 3, None, True, False, {"nested": "dict"}]
    element_id = 'test-id-2'
    expected_output = format_html('<script id="{}" type="application/json">[1, 2, 3, null, true, false, {"nested": "dict"}]</script>', element_id)
    assert json_script(value, element_id) == expected_output

    # Test case 3: Empty dictionary
    value = {}
    element_id = 'test-id-3'
    expected_output = format_html('<script id="{}" type="application/json">{}</script>', element_id, mark_safe('{}'))
    assert json_script(value, element_id) == expected_output

    # Test case 4: Special characters in strings
    value = {'key': '<script>alert("XSS")</script>'}
    element_id = 'test-id-4'
    expected_output = format_html('<script id="{}" type="application/json">{{"key": "&#x3C;script&#x3E;alert(&#x22;XSS&#x22;)</script>&#x3C;/script&#x3E;"}}</script>', element_id)
    assert json_script(value, element_id) == expected_output

    # Test case 5: Non-serializable values (should not raise an error, will be excluded)
    value = {'key': object()}
    element_id = 'test-id-5'
    with pytest.raises(TypeError):
        json_script(value, element_id)