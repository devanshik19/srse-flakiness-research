import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    valid_ips = [
        '192.168.1.1',
        '255.255.255.255',
        '0.0.0.0',
        '8.8.8.8'
    ]
    
    for ip in valid_ips:
        try:
            validate_ipv4_address(ip)
        except ValidationError:
            pytest.fail(f'ValidationError raised for valid IP: {ip}')

def test_validate_ipv4_address_invalid():
    invalid_ips = [
        '256.256.256.256',
        '192.168.1',
        '192.168.1.1.1',
        'abc.def.ghi.jkl',
        ''
    ]
    
    for ip in invalid_ips:
        with pytest.raises(ValidationError):
            validate_ipv4_address(ip)