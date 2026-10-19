import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.core.validators import validate_ipv4_address, validate_ipv6_address

def test_validate_ipv46_address_valid_ipv4():
    valid_ipv4 = '192.168.1.1'
    try:
        validate_ipv46_address(valid_ipv4)
    except ValidationError:
        pytest.fail(f"ValidationError raised for valid IPv4: {valid_ipv4}")

def test_validate_ipv46_address_valid_ipv6():
    valid_ipv6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
    try:
        validate_ipv46_address(valid_ipv6)
    except ValidationError:
        pytest.fail(f"ValidationError raised for valid IPv6: {valid_ipv6}")

def test_validate_ipv46_address_invalid():
    invalid_addresses = [
        '256.256.256.256',  # Invalid IPv4
        '2001:db8:85a3::8a2e:0370:7334g',  # Invalid IPv6
        'invalid_address',  # Non-IP address
        '',  # Empty string
    ]
    for address in invalid_addresses:
        with pytest.raises(ValidationError):
            validate_ipv46_address(address)