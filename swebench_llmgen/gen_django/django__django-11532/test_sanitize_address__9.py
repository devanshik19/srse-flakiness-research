import pytest
from django.core.mail.message import sanitize_address
from email.header import Header
from email.headerregistry import Address

def test_sanitize_address_valid_email():
    result = sanitize_address('test@example.com', 'utf-8')
    expected = str(Address(addr_spec='test@example.com'))
    assert result == expected

def test_sanitize_address_valid_email_with_name():
    result = sanitize_address(('Test User', 'test@example.com'), 'utf-8')
    expected = str(Address(name='Test User', addr_spec='test@example.com'))
    assert result == expected

def test_sanitize_address_invalid_email():
    with pytest.raises(ValueError, match='Invalid address "invalid_email"'):
        sanitize_address('invalid_email', 'utf-8')

def test_sanitize_address_invalid_email_name():
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(('Invalid Name', 'invalid_email'), 'utf-8')

def test_sanitize_address_unicode_email():
    result = sanitize_address('usér@example.com', 'utf-8')
    expected = str(Address(addr_spec='usér@example.com'))
    assert result == expected

def test_sanitize_address_unicode_name():
    result = sanitize_address(('Usér Name', 'user@example.com'), 'utf-8')
    expected = str(Address(name='Usér Name', addr_spec='user@example.com'))
    assert result == expected

def test_sanitize_address_invalid_ascii_localpart():
    with pytest.raises(ValueError):
        sanitize_address(('User Name', 'usér@domain.com'), 'ascii')

def test_sanitize_address_invalid_ascii_domain():
    with pytest.raises(ValueError):
        sanitize_address(('User Name', 'user@domain.ünicode'), 'ascii')