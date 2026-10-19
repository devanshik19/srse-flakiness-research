import pytest
from django.db.models.query_utils import RegisterLookupMixin
from django.contrib.auth.models import User

class TestRegisterLookupMixin(RegisterLookupMixin):
    class_lookups = {}

def test_unregister_lookup_removes_lookup():
    # Arrange: create a lookup and register it
    lookup_name = 'custom_lookup'
    lookup = type('Lookup', (), {'lookup_name': lookup_name})
    TestRegisterLookupMixin.class_lookups[lookup_name] = lookup

    # Act: unregister the lookup
    TestRegisterLookupMixin._unregister_lookup(TestRegisterLookupMixin, lookup)

    # Assert: check that the lookup has been removed
    assert lookup_name not in TestRegisterLookupMixin.class_lookups

def test_unregister_lookup_with_none_lookup_name():
    # Arrange: create a lookup and register it
    lookup_name = 'another_custom_lookup'
    lookup = type('Lookup', (), {'lookup_name': lookup_name})
    TestRegisterLookupMixin.class_lookups[lookup_name] = lookup

    # Act: unregister the lookup with None as lookup_name
    TestRegisterLookupMixin._unregister_lookup(TestRegisterLookupMixin, lookup, None)

    # Assert: check that the lookup has been removed
    assert lookup_name not in TestRegisterLookupMixin.class_lookups