import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    # Test valid IPv4 addresses
    valid_addresses = [
        "192.168.1.1",
        "255.255.255.255",
        "0.0.0.0",
        "8.8.8.8",
        "127.0.0.1"
    ]
    for address in valid_addresses:
        try:
            validate_ipv4_address(address)
        except ValidationError:
            pytest.fail(f"ValidationError raised for valid address: {address}")

def test_validate_ipv4_address_invalid():
    # Test invalid IPv4 addresses
    invalid_addresses = [
        "256.256.256.256",  # Out of range
        "192.168.1.256",    # Out of range
        "192.168.1",        # Incomplete address
        "abc.def.ghi.jkl",  # Non-numeric
        "192.168.1.1.1",     # Too many parts
        "",                  # Empty
        "1234.123.123.123",  # Out of range
        "192.168.-1.1",      # Negative number
    ]
    for address in invalid_addresses:
        with pytest.raises(ValidationError):
            validate_ipv4_address(address)