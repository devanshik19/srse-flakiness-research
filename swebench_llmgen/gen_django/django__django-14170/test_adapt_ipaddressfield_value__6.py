import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations:
    def setup_method(self):
        self.operations = BaseDatabaseOperations()

    def test_adapt_ipaddressfield_value_with_valid_ip(self):
        ip_address = "192.168.1.1"
        result = self.operations.adapt_ipaddressfield_value(ip_address)
        assert result == ip_address

    def test_adapt_ipaddressfield_value_with_empty_string(self):
        result = self.operations.adapt_ipaddressfield_value("")
        assert result is None

    def test_adapt_ipaddressfield_value_with_none(self):
        result = self.operations.adapt_ipaddressfield_value(None)
        assert result is None

    def test_adapt_ipaddressfield_value_with_invalid_ip(self):
        invalid_ip = "999.999.999.999"
        result = self.operations.adapt_ipaddressfield_value(invalid_ip)
        assert result == invalid_ip