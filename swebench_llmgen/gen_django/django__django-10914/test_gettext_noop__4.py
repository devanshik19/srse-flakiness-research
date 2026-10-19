import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test a standard string
    input_string = "Hello, World!"
    assert gettext_noop(input_string) == input_string

    # Test an empty string
    input_string = ""
    assert gettext_noop(input_string) == input_string

    # Test a string with special characters
    input_string = "Hello, 世界!"
    assert gettext_noop(input_string) == input_string

    # Test a numeric string
    input_string = "12345"
    assert gettext_noop(input_string) == input_string

    # Test a multi-line string
    input_string = "Line 1\nLine 2\nLine 3"
    assert gettext_noop(input_string) == input_string