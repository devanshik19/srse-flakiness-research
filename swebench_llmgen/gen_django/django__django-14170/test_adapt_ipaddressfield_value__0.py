import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

def test_adapt_ipaddressfield_value():
    operations = BaseDatabaseOperations(None)
    
    # Test with a valid IP address string
    assert operations.adapt_ipaddressfield_value("192.168.1.1") == "192.168.1.1"
    
    # Test with an empty string
    assert operations.adapt_ipaddressfield_value("") is None
    
    # Test with None
    assert operations.adapt_ipaddressfield_value(None) is None
    
    # Test with an invalid IP address string
    assert operations.adapt_ipaddressfield_value("invalid_ip") == "invalid_ip"