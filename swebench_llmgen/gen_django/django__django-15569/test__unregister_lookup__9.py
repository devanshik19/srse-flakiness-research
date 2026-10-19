import pytest
from django.db.models.query_utils import RegisterLookupMixin
from django.contrib.auth.models import User

class TestRegisterLookupMixin(RegisterLookupMixin):

    def test_unregister_lookup(self):
        # Arrange
        class MockLookup:
            lookup_name = 'mock_lookup'

        # Register a lookup
        lookup = MockLookup()
        self.register_lookup(lookup)

        # Ensure the lookup is registered
        assert 'mock_lookup' in self.class_lookups

        # Act
        self._unregister_lookup(MockLookup)

        # Assert
        assert 'mock_lookup' not in self.class_lookups

    def test_unregister_lookup_with_custom_name(self):
        # Arrange
        class AnotherMockLookup:
            lookup_name = 'another_mock_lookup'

        # Register a lookup
        lookup = AnotherMockLookup()
        self.register_lookup(lookup)

        # Ensure the lookup is registered
        assert 'another_mock_lookup' in self.class_lookups

        # Act
        self._unregister_lookup(AnotherMockLookup, lookup_name='another_mock_lookup')

        # Assert
        assert 'another_mock_lookup' not in self.class_lookups

    def test_unregister_non_existent_lookup(self):
        # Arrange
        class NonExistentLookup:
            lookup_name = 'non_existent'

        # Act & Assert
        with pytest.raises(KeyError):
            self._unregister_lookup(NonExistentLookup)