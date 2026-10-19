import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    assert gettext_noop("Hello, World!") == "Hello, World!"
    assert gettext_noop("") == ""
    assert gettext_noop("foo") == "foo"
    assert gettext_noop("123") == "123"
    assert gettext_noop("!@#$%^&*()") == "!@#$%^&*()"