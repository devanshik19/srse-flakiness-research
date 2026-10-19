import pytest
from django.utils.encoding import force_str
from email.header import Header
from email.headerregistry import Address
from email.errors import HeaderParseError
from django.core.mail.message import sanitize_address

def test_sanitize_address_valid_email():
    assert sanitize_address("user@example.com", "utf-8") == str(Address("user", username="user", domain="example.com"))

def test_sanitize_address_valid_email_with_name():
    assert sanitize_address(("User Name", "user@example.com"), "utf-8") == str(Address("User Name", username="user", domain="example.com"))

def test_sanitize_address_invalid_email_format():
    with pytest.raises(ValueError, match='Invalid address "invalid-email"'):
        sanitize_address("invalid-email", "utf-8")

def test_sanitize_address_invalid_email_with_invalid_name():
    with pytest.raises(ValueError, match='Invalid adddress; only user could be parsed from "User <user@example.com>"'):
        sanitize_address("User <user@example.com>", "utf-8")

def test_sanitize_address_non_ascii_email():
    assert sanitize_address(("Test Üser", "test@example.com"), "utf-8") == str(Address(Header("Test Üser", "utf-8"), username="test", domain="example.com"))

def test_sanitize_address_empty_name():
    assert sanitize_address((" ", "user@example.com"), "utf-8") == str(Address(Header(" ", "utf-8"), username="user", domain="example.com"))