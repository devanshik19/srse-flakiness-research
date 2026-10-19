import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import (
    parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit,
)
from django.utils.encoding import punycode
from django.utils.functional import Promise, keep_lazy, keep_lazy_text
from django.utils.http import RFC3986_GENDELIMS, RFC3986_SUBDELIMS
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import SafeData, SafeString, mark_safe
from django.utils.text import normalize_newlines
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import format_html
import pytest
from django.contrib.auth.models import User

# focal function
def json_script(value, element_id):
    json_str = json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
    return format_html(
        '<script id="{}" type="application/json">{}</script>',
        element_id, mark_safe(json_str)
    )

# Test for the json_script function
def test_json_script():
    # Test cases
    test_value = {"key": "value", "number": 123, "list": [1, 2, 3]}
    element_id = "test-id"
    
    expected_output = (
        '<script id="test-id" type="application/json">'
        '{"key": "value", "number": 123, "list": [1, 2, 3]}'
        '</script>'
    )

    result = json_script(test_value, element_id)
    assert result == expected_output

    # Test with special characters in JSON
    special_value = {"special": "<>&\"'"}
    expected_output_special = (
        '<script id="test-id" type="application/json">'
        '{"special": "<>&\\"\'"}'
        '</script>'
    )

    result_special = json_script(special_value, element_id)
    assert result_special == expected_output_special

    # Testing with empty dictionary
    empty_value = {}
    expected_output_empty = '<script id="test-id" type="application/json">{}</script>'
    
    result_empty = json_script(empty_value, element_id)
    assert result_empty == expected_output_empty