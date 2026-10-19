import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.core.validators import validate_ipv4_address, validate_ipv6_address

def test_validate_ipv46_address_valid_ipv4():
    # Test valid IPv4 address
    value = '192.168.1.1'
    try:
        validate_ipv46_address(value)
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv4 address")

def test_validate_ipv46_address_valid_ipv6():
    # Test valid IPv6 address
    value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
    try:
        validate_ipv46_address(value)
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv6 address")

def test_validate_ipv46_address_invalid_ipv4():
    # Test invalid IPv4 address
    value = '256.256.256.256'
    with pytest.raises(ValidationError) as excinfo:
        validate_ipv46_address(value)
    assert str(excinfo.value) == 'Enter a valid IPv4 or IPv6 address.'

def test_validate_ipv46_address_invalid_ipv6():
    # Test invalid IPv6 address
    value = '2001:db8::g123'
    with pytest.raises(ValidationError) as excinfo:
        validate_ipv46_address(value)
    assert str(excinfo.value) == 'Enter a valid IPv4 or IPv6 address.'

def test_validate_ipv46_address_empty_string():
    # Test empty string input
    value = ''
    with pytest.raises(ValidationError) as excinfo:
        validate_ipv46_address(value)
    assert str(excinfo.value) == 'Enter a valid IPv4 or IPv6 address.'