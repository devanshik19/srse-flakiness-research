import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address

def test_validate_ipv46_address_valid_ipv4():
    assert validate_ipv46_address('192.168.1.1') is None

def test_validate_ipv46_address_valid_ipv6():
    assert validate_ipv46_address('::1') is None

def test_validate_ipv46_address_invalid_ipv4():
    with pytest.raises(ValidationError, match='Enter a valid IPv4 or IPv6 address.'):
        validate_ipv46_address('999.999.999.999')

def test_validate_ipv46_address_invalid_ipv6():
    with pytest.raises(ValidationError, match='Enter a valid IPv4 or IPv6 address.'):
        validate_ipv46_address('invalid::address')

def test_validate_ipv46_address_empty_string():
    with pytest.raises(ValidationError, match='Enter a valid IPv4 or IPv6 address.'):
        validate_ipv46_address('')