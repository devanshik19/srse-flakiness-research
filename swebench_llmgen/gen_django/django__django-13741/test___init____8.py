import pytest
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_read_only_password_hash_field_init():
    # Test with default arguments
    field = ReadOnlyPasswordHashField()
    assert field.required is False

    # Test with required set to True
    field_with_required = ReadOnlyPasswordHashField(required=True)
    assert field_with_required.required is True

    # Test with additional arguments
    field_with_extra_args = ReadOnlyPasswordHashField(label='Password', initial='my_initial')
    assert field_with_extra_args.label == 'Password'
    assert field_with_extra_args.initial == 'my_initial'
    assert field_with_extra_args.required is False  # Ensure required is False by default