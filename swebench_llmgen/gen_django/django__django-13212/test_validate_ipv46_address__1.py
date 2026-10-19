import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.utils.translation import gettext_lazy as _

def test_validate_ipv46_address_valid_ipv4():
    validate_ipv46_address("192.168.1.1")  # Should not raise an exception

def test_validate_ipv46_address_valid_ipv6():
    validate_ipv46_address("::1")  # Should not raise an exception

def test_validate_ipv46_address_invalid_ipv4():
    with pytest.raises(ValidationError, match=str(_('Enter a valid IPv4 or IPv6 address.'))):
        validate_ipv46_address("999.999.999.999")  # Invalid IPv4

def test_validate_ipv46_address_invalid_ipv6():
    with pytest.raises(ValidationError, match=str(_('Enter a valid IPv4 or IPv6 address.'))):
        validate_ipv46_address("invalid:ipv6::address")  # Invalid IPv6

def test_validate_ipv46_address_empty():
    with pytest.raises(ValidationError, match=str(_('Enter a valid IPv4 or IPv6 address.'))):
        validate_ipv46_address("")  # Empty string