import pytest
from email.header import Header
from django.core.mail.message import sanitize_address

def test_sanitize_address_valid_email():
    assert sanitize_address("user@example.com", "utf-8") == 'user@example.com'

def test_sanitize_address_valid_tuple():
    assert sanitize_address(("User Name", "user@example.com"), "utf-8") == 'User Name <user@example.com>'

def test_sanitize_address_invalid_email_no_at_symbol():
    with pytest.raises(ValueError, match='Invalid address "invalid_email"'):
        sanitize_address("invalid_email", "utf-8")

def test_sanitize_address_invalid_email_too_many_parts():
    with pytest.raises(ValueError, match='Invalid adddress; only user could be parsed from "user@example.com extra"'):
        sanitize_address("user@example.com extra", "utf-8")

def test_sanitize_address_invalid_tuple():
    with pytest.raises(ValueError):
        sanitize_address(("User Name", "invalid_email"), "utf-8")

def test_sanitize_address_encoded_name():
    assert sanitize_address(("User Name 😊", "user@example.com"), "utf-8") == '=?utf-8?b?VXNlciBOYW1lIOKcqA==?= <user@example.com>'