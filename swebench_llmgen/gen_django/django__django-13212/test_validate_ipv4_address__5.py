import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    valid_addresses = [
        '192.168.1.1',
        '255.255.255.255',
        '0.0.0.0',
        '127.0.0.1'
    ]
    
    for address in valid_addresses:
        try:
            validate_ipv4_address(address)
        except ValidationError:
            pytest.fail(f"ValidationError raised for valid address: {address}")

def test_validate_ipv4_address_invalid():
    invalid_addresses = [
        '256.100.50.25',  # Invalid octet
        '192.168.1',      # Incomplete address
        '192.168.1.1.1',  # Too many octets
        'abc.def.ghi.jkl',  # Non-numeric input
        '',               # Empty string
        None              # None value
    ]

    for address in invalid_addresses:
        with pytest.raises(ValidationError, match=str(_('Enter a valid IPv4 address.'))):
            validate_ipv4_address(address)