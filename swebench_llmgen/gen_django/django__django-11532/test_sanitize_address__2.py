import pytest
from email.header import Header
from email.headerregistry import Address
from django.core.mail.message import sanitize_address

def test_sanitize_address_valid_email():
    addr = "test@example.com"
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    expected = str(Address('', username='test', domain='example.com'))
    assert result == expected

def test_sanitize_address_valid_tuple():
    addr = ("Test User", "test@example.com")
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    expected = str(Address('Test User', username='test', domain='example.com'))
    assert result == expected

def test_sanitize_address_invalid_email():
    addr = "invalid-email"
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, encoding)

def test_sanitize_address_invalid_tuple():
    addr = ("Test User", "invalid-email")
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(addr, encoding)

def test_sanitize_address_email_with_display_name():
    addr = ("Test User", "test@example.com")
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    expected = str(Address('Test User', username='test', domain='example.com'))
    assert result == expected

def test_sanitize_address_localpart_unsupported_encoding():
    addr = ("Test User", "tést@example.com")
    encoding = 'ascii'
    result = sanitize_address(addr, encoding)
    expected = str(Address('Test User', username='tést', domain='example.com'))
    assert result == expected

def test_sanitize_address_domain_idna_encoding():
    addr = ("Test User", "test@español.com")
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    expected = str(Address('Test User', username='test', domain='xn--espaol-zwa.com'))
    assert result == expected