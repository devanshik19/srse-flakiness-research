import pytest
from django.db.models.query_utils import RegisterLookupMixin
from django.contrib.auth.models import User

class TestRegisterLookupMixin(RegisterLookupMixin):
    class_lookups = {}

def test_unregister_lookup_removes_lookup():
    # Arrange
    test_mixin = TestRegisterLookupMixin()
    lookup_name = 'custom_lookup'
    lookup = type('Lookup', (object,), {'lookup_name': lookup_name})
    test_mixin.class_lookups[lookup_name] = lookup
    
    # Act
    test_mixin._unregister_lookup(lookup)

    # Assert
    assert lookup_name not in test_mixin.class_lookups

def test_unregister_lookup_with_none_lookup_name_removes_lookup():
    # Arrange
    test_mixin = TestRegisterLookupMixin()
    lookup_name = 'another_custom_lookup'
    lookup = type('Lookup', (object,), {'lookup_name': lookup_name})
    test_mixin.class_lookups[lookup_name] = lookup
    
    # Act
    test_mixin._unregister_lookup(lookup, None)

    # Assert
    assert lookup_name not in test_mixin.class_lookups

def test_unregister_lookup_raises_key_error_if_lookup_not_registered():
    # Arrange
    test_mixin = TestRegisterLookupMixin()
    lookup_name = 'non_existent_lookup'
    lookup = type('Lookup', (object,), {'lookup_name': lookup_name})

    # Act & Assert
    with pytest.raises(KeyError):
        test_mixin._unregister_lookup(lookup)