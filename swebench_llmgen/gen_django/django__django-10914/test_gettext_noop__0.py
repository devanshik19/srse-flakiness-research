import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("test") == "test"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a string containing special characters
    assert gettext_noop("Hello, World! @2023") == "Hello, World! @2023"
    
    # Test with a string containing Unicode characters
    assert gettext_noop("こんにちは") == "こんにちは"
    
    # Test with a string containing digits
    assert gettext_noop("12345") == "12345"