import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a normal string
    assert gettext_noop("Hello, world!") == "Hello, world!"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a string containing special characters
    assert gettext_noop("Hello, 🌍!") == "Hello, 🌍!"
    
    # Test with a string containing numbers
    assert gettext_noop("Number 12345") == "Number 12345"
    
    # Test with a string containing unicode characters
    assert gettext_noop("こんにちは") == "こんにちは"