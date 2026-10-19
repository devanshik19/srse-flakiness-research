import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test that gettext_noop returns the input string as is
    input_str = "Hello, world!"
    assert gettext_noop(input_str) == input_str
    
    # Test with an empty string
    assert gettext_noop("") == ""
    
    # Test with a numeric string
    numeric_str = "12345"
    assert gettext_noop(numeric_str) == numeric_str
    
    # Test with a special characters string
    special_str = "!@#$%^&*()"
    assert gettext_noop(special_str) == special_str