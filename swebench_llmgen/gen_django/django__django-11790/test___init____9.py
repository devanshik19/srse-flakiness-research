import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_without_required_argument(self):
        field = ReadOnlyPasswordHashField()
        assert not field.required

    def test_init_with_required_argument(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required

    def test_init_with_default_false_required_argument(self):
        field = ReadOnlyPasswordHashField(required=False)
        assert not field.required