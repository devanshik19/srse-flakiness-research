import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    # Test with a simple string
    assert gettext_noop("test string") == "test string"

    # Test with an empty string
    assert gettext_noop("") == ""

    # Test with a string containing special characters
    assert gettext_noop("string with special chars !@#") == "string with special chars !@#"

    # Test with a unicode string
    assert gettext_noop("unicode string: ñ, ü, 中, 😊") == "unicode string: ñ, ü, 中, 😊"