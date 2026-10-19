import pytest
from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    assert gettext_noop("Hello, World!") == "Hello, World!"
    assert gettext_noop("") == ""
    assert gettext_noop("Django is great!") == "Django is great!"
    assert gettext_noop("12345") == "12345"
    assert gettext_noop("Hello, 世界!") == "Hello, 世界!"