import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("Hello, World!") == "Hello, World!"
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a numeric string
    assert gettext_noop("12345") == "12345"
    
    # Test with a special character string
    assert gettext_noop("!@#$%^&*()") == "!@#$%^&*()"
    
    # Test with a unicode string
    unicode_string = "こんにちは"  # "Hello" in Japanese
    assert gettext_noop(unicode_string) == unicode_string