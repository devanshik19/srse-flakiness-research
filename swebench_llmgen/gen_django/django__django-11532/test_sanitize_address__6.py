import pytest
from django.core.mail.message import sanitize_address

def test_sanitize_address_valid_tuple():
    addr = ('John Doe', 'john.doe@example.com')
    result = sanitize_address(addr, 'utf-8')
    assert result == 'John Doe <john.doe@example.com>'

def test_sanitize_address_valid_string():
    addr = 'john.doe@example.com'
    result = sanitize_address(addr, 'utf-8')
    assert result == 'john.doe@example.com'

def test_sanitize_address_invalid_address_no_at_symbol():
    addr = 'johndoeexample.com'
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_invalid_address_partial():
    addr = 'John Doe <john.doe@example.com'
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_invalid_address_tuple():
    addr = ('John Doe', 'invalid-email.com')
    with pytest.raises(ValueError):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_non_ascii_name():
    addr = ('José', 'jose@example.com')
    result = sanitize_address(addr, 'utf-8')
    assert result == '=?utf-8?q?Jos=C3=A9?= <jose@example.com>'