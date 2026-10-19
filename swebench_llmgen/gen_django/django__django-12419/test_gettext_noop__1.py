import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    result = gettext_noop("Hello, World!")
    assert result == "Hello, World!"

    # Test with an empty string
    result = gettext_noop("")
    assert result == ""

    # Test with a string containing special characters
    result = gettext_noop("Hello, 🌍!")
    assert result == "Hello, 🌍!"

    # Test with a numeric string
    result = gettext_noop("12345")
    assert result == "12345"