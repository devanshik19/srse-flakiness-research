import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations:

    @pytest.fixture
    def db_operations(self):
        return BaseDatabaseOperations(connection=None)

    def test_adapt_ipaddressfield_value_none(self, db_operations):
        # Test passing None
        result = db_operations.adapt_ipaddressfield_value(None)
        assert result is None

    def test_adapt_ipaddressfield_value_empty_string(self, db_operations):
        # Test passing an empty string
        result = db_operations.adapt_ipaddressfield_value("")
        assert result == ""

    def test_adapt_ipaddressfield_value_valid_ip(self, db_operations):
        # Test passing a valid IP address string
        result = db_operations.adapt_ipaddressfield_value("192.168.1.1")
        assert result == "192.168.1.1"

    def test_adapt_ipaddressfield_value_invalid_ip(self, db_operations):
        # Test passing an invalid IP address string
        result = db_operations.adapt_ipaddressfield_value("999.999.999.999")
        assert result == "999.999.999.999"