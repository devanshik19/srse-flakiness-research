import pytest
from django.core.mail.message import sanitize_address
from email.header import Header
from email.headerregistry import Address

def test_sanitize_address_valid_string():
    addr = "John Doe <john@example.com>"
    encoding = 'utf-8'
    expected = str(Address("John Doe", username="john", domain="example.com"))
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_valid_tuple():
    addr = ("John Doe", "john@example.com")
    encoding = 'utf-8'
    expected = str(Address("John Doe", username="john", domain="example.com"))
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_invalid_address_string():
    addr = "invalid-address"
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, encoding)

def test_sanitize_address_invalid_address_tuple():
    addr = ("John Doe", "invalid-email")
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(addr, encoding)

def test_sanitize_address_address_with_non_ascii_name():
    addr = ("Jöhn Dœ", "john@example.com")
    encoding = 'utf-8'
    expected = str(Address("Jöhn Dœ", username="john", domain="example.com"))
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_address_with_non_ascii_local_part():
    addr = "Jöhn Dœ <jöhn@example.com>"
    encoding = 'utf-8'
    expected = str(Address("Jöhn Dœ", username="jöhn", domain="example.com"))
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_address_with_idna_domain():
    addr = "John Doe <john@xn--exmple-54a.com>"
    encoding = 'utf-8'
    expected = str(Address("John Doe", username="john", domain="例.com"))
    result = sanitize_address(addr, encoding)
    assert result == expected