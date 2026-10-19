import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a normal string
    input_str = "Hello, World!"
    assert gettext_noop(input_str) == input_str

    # Test with an empty string
    input_str_empty = ""
    assert gettext_noop(input_str_empty) == input_str_empty

    # Test with a string that includes special characters
    input_str_special = "Hello, World! @#$%^&*()"
    assert gettext_noop(input_str_special) == input_str_special

    # Test with a string containing numbers
    input_str_numbers = "1234567890"
    assert gettext_noop(input_str_numbers) == input_str_numbers

    # Test with a long string
    input_str_long = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
                     "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    assert gettext_noop(input_str_long) == input_str_long