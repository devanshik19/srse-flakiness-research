import pytest
from django.core.mail.message import sanitize_address
from email.errors import HeaderParseError

def test_sanitize_address_valid_email():
    # Test with a regular email address
    addr = "John Doe <john.doe@example.com>"
    result = sanitize_address(addr, 'utf-8')
    expected = 'John Doe <john.doe@example.com>'
    assert result == expected

def test_sanitize_address_valid_tuple():
    # Test with a tuple (name, email)
    addr = ("John Doe", "john.doe@example.com")
    result = sanitize_address(addr, 'utf-8')
    expected = 'John Doe <john.doe@example.com>'
    assert result == expected

def test_sanitize_address_invalid_email_empty():
    # Test with an empty email address
    addr = ""
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_invalid_email_malformed():
    # Test with a malformed email address
    addr = "invalid-email"
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_invalid_address_wrong_format():
    # Test with an incorrectly formatted address
    addr = "John Doe <john.doe@example> @"
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(addr, 'utf-8')

def test_sanitize_address_special_characters():
    # Test with special characters in name
    addr = "Jöhn Dœ <john.doe@example.com>"
    result = sanitize_address(addr, 'utf-8')
    expected = 'Jöhn Dœ <john.doe@example.com>'
    assert result == expected