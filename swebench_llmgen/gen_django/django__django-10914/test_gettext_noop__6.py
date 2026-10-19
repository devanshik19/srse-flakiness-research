import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("Hello, World!") == "Hello, World!"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with numeric string
    assert gettext_noop("12345") == "12345"
    
    # Test with special characters
    assert gettext_noop("!@#$%^&*()") == "!@#$%^&*()"
    
    # Test with a long string
    long_string = "This is a long string " * 100
    assert gettext_noop(long_string) == long_string