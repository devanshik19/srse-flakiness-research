import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_required_false(self):
        field = ReadOnlyPasswordHashField()
        assert not field.required

    def test_init_with_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required

    def test_init_with_custom_arguments(self):
        field = ReadOnlyPasswordHashField(label='Custom Label', help_text='Custom Help Text', required=True)
        assert field.label == 'Custom Label'
        assert field.help_text == 'Custom Help Text'
        assert field.required