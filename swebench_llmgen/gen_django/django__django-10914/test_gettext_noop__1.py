import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test case 1: Normal string input
    input_str = "Hello, World!"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test case 2: Empty string input
    input_str = ""
    result = gettext_noop(input_str)
    assert result == input_str

    # Test case 3: String with special characters
    input_str = "Special characters: !@#$%^&*()"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test case 4: Numeric string input
    input_str = "12345"
    result = gettext_noop(input_str)
    assert result == input_str

    # Test case 5: Multi-line string input
    input_str = """This is line one.
This is line two.
This is line three."""
    result = gettext_noop(input_str)
    assert result == input_str