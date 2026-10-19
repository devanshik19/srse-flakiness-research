import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    assert gettext_noop("test") == "test"
    assert gettext_noop("") == ""
    assert gettext_noop("こんにちは") == "こんにちは"
    assert gettext_noop("123") == "123"