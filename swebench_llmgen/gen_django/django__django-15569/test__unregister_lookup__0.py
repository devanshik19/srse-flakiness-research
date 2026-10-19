import pytest
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models import Lookup
from django.contrib.auth.models import User

class CustomLookup(Lookup):
    lookup_name = 'custom'

class TestRegisterLookupMixin(RegisterLookupMixin):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.class_lookups = {}
        cls.register_lookup(CustomLookup)

    def test_unregister_lookup(self):
        # Ensure the lookup is registered first
        assert 'custom' in self.class_lookups

        # Unregister the lookup using the function
        self._unregister_lookup(CustomLookup)

        # Check that the lookup has been removed
        assert 'custom' not in self.class_lookups

    def test_unregister_lookup_with_name(self):
        # Ensure the lookup is registered first
        assert 'custom' in self.class_lookups

        # Unregister the lookup using the lookup name
        self._unregister_lookup(CustomLookup, 'custom')

        # Check that the lookup has been removed
        assert 'custom' not in self.class_lookups

    def test_unregister_nonexistent_lookup(self):
        # Remove a non-existent lookup
        self._unregister_lookup(CustomLookup, 'nonexistent')

        # Check that no error occurs and the state is unchanged
        assert 'custom' in self.class_lookups