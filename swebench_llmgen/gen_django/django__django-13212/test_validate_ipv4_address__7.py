import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def test_validate_ipv4_address_valid():
    try:
        validate_ipv4_address('192.168.1.1')
    except ValidationError:
        pytest.fail("ValidationError was raised for a valid IPv4 address.")

def test_validate_ipv4_address_invalid():
    with pytest.raises(ValidationError) as excinfo:
        validate_ipv4_address('256.256.256.256')
    assert str(excinfo.value) == 'Enter a valid IPv4 address.'

    with pytest.raises(ValidationError) as excinfo:
        validate_ipv4_address('192.168.1')
    assert str(excinfo.value) == 'Enter a valid IPv4 address.'

    with pytest.raises(ValidationError) as excinfo:
        validate_ipv4_address('not.an.ip')
    assert str(excinfo.value) == 'Enter a valid IPv4 address.'