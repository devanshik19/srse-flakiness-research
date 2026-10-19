import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import RegisterLookupMixin

class MockLookup:
    def __init__(self, name):
        self.lookup_name = name

def test_unregister_lookup_removes_lookup():
    # Arrange
    mixin = RegisterLookupMixin
    lookup = MockLookup('my_lookup')
    
    # Register the lookup first
    mixin.class_lookups = {'my_lookup': lookup}
    
    # Act
    mixin._unregister_lookup(lookup)

    # Assert
    assert 'my_lookup' not in mixin.class_lookups

def test_unregister_lookup_removes_lookup_by_name():
    # Arrange
    mixin = RegisterLookupMixin
    lookup = MockLookup('my_other_lookup')

    # Register the lookup first
    mixin.class_lookups = {'my_other_lookup': lookup}
    
    # Act
    mixin._unregister_lookup(lookup, 'my_other_lookup')

    # Assert
    assert 'my_other_lookup' not in mixin.class_lookups

def test_unregister_lookup_raises_key_error_when_not_found():
    # Arrange
    mixin = RegisterLookupMixin
    mixin.class_lookups = {}
    lookup = MockLookup('not_registered_lookup')

    # Act & Assert
    with pytest.raises(KeyError):
        mixin._unregister_lookup(lookup)