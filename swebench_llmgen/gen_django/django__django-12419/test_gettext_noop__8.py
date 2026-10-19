import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    input_str = "Hello, World!"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test with an empty string
    input_str = ""
    result = gettext_noop(input_str)
    assert result == input_str

    # Test with a string containing special characters
    input_str = "¡Hola, Mundo!"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test with a unicode string
    input_str = "你好，世界！"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test with a string that has numbers
    input_str = "The year is 2023."
    result = gettext_noop(input_str)
    assert result == input_str