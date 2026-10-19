import pytest
from django.db.models.query_utils import RegisterLookupMixin
from django.contrib.auth.models import User

class CustomLookup:
    lookup_name = 'custom_lookup'

class TestRegisterLookupMixin(RegisterLookupMixin):
    pass

def test_unregister_lookup():
    # Arrange
    mixin_instance = TestRegisterLookupMixin()
    custom_lookup = CustomLookup()
    mixin_instance.register_lookup(custom_lookup)

    # Act
    mixin_instance._unregister_lookup(CustomLookup)

    # Assert
    with pytest.raises(KeyError):
        mixin_instance.get_lookups().get('custom_lookup')

def test_unregister_lookup_with_name():
    # Arrange
    mixin_instance = TestRegisterLookupMixin()
    custom_lookup = CustomLookup()
    mixin_instance.register_lookup(custom_lookup)

    # Act
    mixin_instance._unregister_lookup(CustomLookup, lookup_name='custom_lookup')

    # Assert
    with pytest.raises(KeyError):
        mixin_instance.get_lookups().get('custom_lookup')