import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("Hello") == "Hello"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a string containing special characters
    assert gettext_noop("Hello, world! @2023") == "Hello, world! @2023"
    
    # Test with a string that is a number
    assert gettext_noop("12345") == "12345"
    
    # Test with a multiline string
    assert gettext_noop("Line 1\nLine 2") == "Line 1\nLine 2"