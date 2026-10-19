import pytest
from django.utils.html import json_script
from django.contrib.auth.models import User
from django.utils.html import format_html

def test_json_script():
    user = User.objects.create_user(username='testuser', password='password123')
    
    # Test with a simple dictionary
    data = {'key': 'value', 'user_id': user.id}
    script = json_script(data, 'test-element')
    expected = format_html(
        '<script id="{}" type="application/json">{}</script>',
        'test-element', mark_safe('{"key": "value", "user_id": 1}')
    )
    assert script == expected

    # Test with a list
    data_list = [1, 2, 3, {"key": "value"}]
    script_list = json_script(data_list, 'test-element-list')
    expected_list = format_html(
        '<script id="{}" type="application/json">{}</script>',
        'test-element-list', mark_safe('[1, 2, 3, {"key": "value"}]')
    )
    assert script_list == expected_list

    # Test with a string
    data_string = "Sample string"
    script_string = json_script(data_string, 'test-element-string')
    expected_string = format_html(
        '<script id="{}" type="application/json">{}</script>',
        'test-element-string', mark_safe('"Sample string"')
    )
    assert script_string == expected_string

    # Test with a boolean value
    data_boolean = True
    script_boolean = json_script(data_boolean, 'test-element-bool')
    expected_boolean = format_html(
        '<script id="{}" type="application/json">{}</script>',
        'test-element-bool', mark_safe('true')
    )
    assert script_boolean == expected_boolean