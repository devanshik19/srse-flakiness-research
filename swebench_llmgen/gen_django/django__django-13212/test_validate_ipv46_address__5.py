import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address


def test_validate_ipv46_address_valid_ipv4():
    # Test valid IPv4 address
    try:
        validate_ipv46_address("192.168.1.1")
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv4 address")


def test_validate_ipv46_address_valid_ipv6():
    # Test valid IPv6 address
    try:
        validate_ipv46_address("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv6 address")


def test_validate_ipv46_address_invalid():
    # Test invalid address
    with pytest.raises(ValidationError, match='Enter a valid IPv4 or IPv6 address.'):
        validate_ipv46_address("invalid_address")


def test_validate_ipv46_address_empty():
    # Test empty input
    with pytest.raises(ValidationError, match='Enter a valid IPv4 or IPv6 address.'):
        validate_ipv46_address("")