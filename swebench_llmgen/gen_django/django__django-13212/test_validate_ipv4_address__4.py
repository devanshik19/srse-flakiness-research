import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    valid_ips = [
        '192.168.1.1',
        '255.255.255.255',
        '0.0.0.0',
        '172.16.254.1'
    ]
    
    for ip in valid_ips:
        try:
            validate_ipv4_address(ip)
        except ValidationError:
            pytest.fail(f"ValidationError raised for valid IP: {ip}")

def test_validate_ipv4_address_invalid():
    invalid_ips = [
        '256.256.256.256',
        '192.168.1.500',
        'abc.def.ghi.jkl',
        '192.168.1',
        '192.168.1.1.1'
    ]
    
    for ip in invalid_ips:
        with pytest.raises(ValidationError) as excinfo:
            validate_ipv4_address(ip)
        assert str(excinfo.value) == str(_('Enter a valid IPv4 address.'))