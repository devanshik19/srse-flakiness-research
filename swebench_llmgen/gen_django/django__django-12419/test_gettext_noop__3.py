import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a regular string
    input_str = "Hello, World!"
    assert gettext_noop(input_str) == input_str

    # Test with an empty string
    input_str_empty = ""
    assert gettext_noop(input_str_empty) == input_str_empty

    # Test with a string containing special characters
    input_str_special = "Special characters: @#$%^&*()!"
    assert gettext_noop(input_str_special) == input_str_special

    # Test with a unicode string
    input_str_unicode = "こんにちは"  # "Hello" in Japanese
    assert gettext_noop(input_str_unicode) == input_str_unicode