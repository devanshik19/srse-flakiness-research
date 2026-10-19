import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    # Test valid IPv4 addresses
    valid_addresses = [
        '192.168.1.1',
        '255.255.255.255',
        '0.0.0.0',
        '172.16.254.1'
    ]
    
    for address in valid_addresses:
        try:
            validate_ipv4_address(address)
        except ValidationError:
            pytest.fail(f'ValidationError raised for valid address: {address}')

def test_validate_ipv4_address_invalid():
    # Test invalid IPv4 addresses
    invalid_addresses = [
        '256.256.256.256',
        '192.168.1.256',
        '192.168.1',
        '192.168.1.1.1',
        'not_an_ip',
        '',
        None,
        '12345'
    ]
    
    for address in invalid_addresses:
        with pytest.raises(ValidationError) as excinfo:
            validate_ipv4_address(address)
        assert str(excinfo.value) == str(_('Enter a valid IPv4 address.'))