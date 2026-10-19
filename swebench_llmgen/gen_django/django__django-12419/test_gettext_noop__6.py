import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    assert gettext_noop("Hello, World!") == "Hello, World!"
    assert gettext_noop("") == ""
    assert gettext_noop("Test string") == "Test string"
    assert gettext_noop("Lorem Ipsum") == "Lorem Ipsum"