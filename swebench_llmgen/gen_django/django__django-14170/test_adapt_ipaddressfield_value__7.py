import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

def test_adapt_ipaddressfield_value():
    operations = BaseDatabaseOperations(None)

    # Test with a valid IP address string
    ip_address = "192.168.1.1"
    result = operations.adapt_ipaddressfield_value(ip_address)
    assert result == ip_address

    # Test with None
    result = operations.adapt_ipaddressfield_value(None)
    assert result is None

    # Test with empty string
    result = operations.adapt_ipaddressfield_value("")
    assert result is None