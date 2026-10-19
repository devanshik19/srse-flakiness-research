import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations:

    @pytest.fixture
    def db_operations(self):
        return BaseDatabaseOperations()

    def test_adapt_ipaddressfield_value_with_valid_ip(self, db_operations):
        result = db_operations.adapt_ipaddressfield_value("192.168.1.1")
        assert result == "192.168.1.1"

    def test_adapt_ipaddressfield_value_with_empty_string(self, db_operations):
        result = db_operations.adapt_ipaddressfield_value("")
        assert result is None

    def test_adapt_ipaddressfield_value_with_none(self, db_operations):
        result = db_operations.adapt_ipaddressfield_value(None)
        assert result is None