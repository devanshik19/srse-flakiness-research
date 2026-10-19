import pytest
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def test_validate_ipv46_address_valid_ipv4():
    try:
        validate_ipv46_address('192.168.1.1')
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv4 address")

def test_validate_ipv46_address_valid_ipv6():
    try:
        validate_ipv46_address('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
    except ValidationError:
        pytest.fail("ValidationError raised for valid IPv6 address")

def test_validate_ipv46_address_invalid():
    with pytest.raises(ValidationError) as excinfo:
        validate_ipv46_address('invalid_ip')
    assert str(excinfo.value) == str(_('Enter a valid IPv4 or IPv6 address.'))

def test_validate_ipv46_address_invalid_ipv4():
    with pytest.raises(ValidationError):
        validate_ipv46_address('256.256.256.256')

def test_validate_ipv46_address_invalid_ipv6():
    with pytest.raises(ValidationError):
        validate_ipv46_address('2001:db8:::1')