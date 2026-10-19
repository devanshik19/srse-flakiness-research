import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations:
    
    @pytest.fixture
    def db_operations(self):
        return BaseDatabaseOperations(None)
    
    def test_adapt_ipaddressfield_value_none(self, db_operations):
        assert db_operations.adapt_ipaddressfield_value(None) is None

    def test_adapt_ipaddressfield_value_empty_string(self, db_operations):
        assert db_operations.adapt_ipaddressfield_value('') is None

    def test_adapt_ipaddressfield_value_valid_ip(self, db_operations):
        valid_ip = '192.168.1.1'
        assert db_operations.adapt_ipaddressfield_value(valid_ip) == valid_ip

    def test_adapt_ipaddressfield_value_invalid_ip(self, db_operations):
        invalid_ip = '999.999.999.999'
        assert db_operations.adapt_ipaddressfield_value(invalid_ip) == invalid_ip