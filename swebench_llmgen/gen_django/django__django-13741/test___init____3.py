import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_readonly_password_hash_field_init():
    # Test the default initialization
    field = ReadOnlyPasswordHashField()
    assert field.required is False

    # Test initialization with required set to True
    field_required = ReadOnlyPasswordHashField(required=True)
    assert field_required.required is True

    # Test initialization with other arguments
    field_with_label = ReadOnlyPasswordHashField(label='Password')
    assert field_with_label.label == 'Password'

    field_with_initial = ReadOnlyPasswordHashField(initial='defaulthash')
    assert field_with_initial.initial == 'defaulthash'