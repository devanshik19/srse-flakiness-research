import pytest
from django.core.mail.message import sanitize_address
from email.errors import HeaderParseError

def test_sanitize_address_valid_string():
    result = sanitize_address("John Doe <john.doe@example.com>", 'utf-8')
    expected = 'John Doe <john.doe@example.com>'
    assert result == expected

def test_sanitize_address_valid_tuple():
    result = sanitize_address(("John Doe", "john.doe@example.com"), 'utf-8')
    expected = 'John Doe <john.doe@example.com>'
    assert result == expected

def test_sanitize_address_invalid_string():
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address("invalid-email", 'utf-8')

def test_sanitize_address_invalid_tuple():
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(("John Doe", "invalid-email"), 'utf-8')

def test_sanitize_address_ascii_only():
    result = sanitize_address(("John Doe", "john_doe@example.com"), 'ascii')
    expected = 'John Doe <john_doe@example.com>'
    assert result == expected

def test_sanitize_address_invalid_name_encoding():
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(("John Doe \udc80", "john.doe@example.com"), 'utf-8')