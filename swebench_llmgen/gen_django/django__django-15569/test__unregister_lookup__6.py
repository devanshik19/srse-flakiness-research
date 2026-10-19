import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import RegisterLookupMixin, LOOKUP_SEP


class TestRegisterLookupMixin(RegisterLookupMixin):
    class_lookups = {}

    @classmethod
    def register_lookup(cls, lookup, lookup_name=None):
        if lookup_name is None:
            lookup_name = lookup.lookup_name
        cls.class_lookups[lookup_name] = lookup


class MockLookup:
    def __init__(self, lookup_name):
        self.lookup_name = lookup_name


def test_unregister_lookup():
    # Arrange
    mixin = TestRegisterLookupMixin()
    lookup = MockLookup('my_lookup')
    mixin.register_lookup(lookup)

    # Assert lookup was registered
    assert 'my_lookup' in mixin.class_lookups

    # Act
    mixin._unregister_lookup(lookup)

    # Assert lookup was unregistered
    assert 'my_lookup' not in mixin.class_lookups


def test_unregister_lookup_with_name():
    # Arrange
    mixin = TestRegisterLookupMixin()
    lookup = MockLookup('another_lookup')
    mixin.register_lookup(lookup)

    # Assert lookup was registered
    assert 'another_lookup' in mixin.class_lookups

    # Act
    mixin._unregister_lookup(lookup, lookup_name='another_lookup')

    # Assert lookup was unregistered
    assert 'another_lookup' not in mixin.class_lookups