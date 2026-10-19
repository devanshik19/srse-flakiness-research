import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("Hello, World!") == "Hello, World!"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a string containing special characters
    assert gettext_noop("This is a test! @#$%^&*()") == "This is a test! @#$%^&*()"
    
    # Test with a numerical string
    assert gettext_noop("12345") == "12345"
    
    # Test with a multi-line string
    assert gettext_noop("Line 1\nLine 2") == "Line 1\nLine 2"