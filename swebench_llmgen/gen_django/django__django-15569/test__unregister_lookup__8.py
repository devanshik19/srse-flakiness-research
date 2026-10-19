import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

class RegisterLookupMixin:
    class_lookups = {}

    def _unregister_lookup(cls, lookup, lookup_name=None):
        if lookup_name is None:
            lookup_name = lookup.lookup_name
        del cls.class_lookups[lookup_name]


class CustomLookup:
    lookup_name = 'custom_lookup'


@pytest.fixture
def setup_lookup():
    # Set up the initial state
    RegisterLookupMixin.class_lookups['custom_lookup'] = CustomLookup


def test_unregister_lookup(setup_lookup):
    assert 'custom_lookup' in RegisterLookupMixin.class_lookups

    # Create an instance of CustomLookup
    lookup_instance = CustomLookup()

    # Unregister the lookup
    RegisterLookupMixin._unregister_lookup(RegisterLookupMixin, lookup_instance)

    # Assert the lookup has been unregistered
    assert 'custom_lookup' not in RegisterLookupMixin.class_lookups


def test_unregister_lookup_with_name(setup_lookup):
    assert 'custom_lookup' in RegisterLookupMixin.class_lookups

    # Unregister the lookup using the lookup name directly
    RegisterLookupMixin._unregister_lookup(RegisterLookupMixin, None, lookup_name='custom_lookup')

    # Assert the lookup has been unregistered
    assert 'custom_lookup' not in RegisterLookupMixin.class_lookups