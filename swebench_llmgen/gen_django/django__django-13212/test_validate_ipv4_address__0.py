import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    # Test valid IPv4 addresses
    valid_ips = [
        '192.168.1.1',
        '0.0.0.0',
        '255.255.255.255',
        '172.16.0.1'
    ]
    
    for ip in valid_ips:
        try:
            validate_ipv4_address(ip)
        except ValidationError:
            pytest.fail(f"ValidationError raised for valid IP: {ip}")

def test_validate_ipv4_address_invalid():
    # Test invalid IPv4 addresses
    invalid_ips = [
        '256.256.256.256',
        '192.168.1',
        '192.168.1.1.1',
        'abc.def.ghi.jkl',
        '123.456.789.0'
    ]
    
    for ip in invalid_ips:
        with pytest.raises(ValidationError):
            validate_ipv4_address(ip)