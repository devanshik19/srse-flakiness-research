import pytest
from email.errors import HeaderParseError
from django.core.mail.message import sanitize_address

def test_sanitize_address_with_valid_string():
    addr = "John Doe <john.doe@example.com>"
    encoding = 'utf-8'
    expected = 'John Doe <john.doe@example.com>'
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_with_valid_tuple():
    addr = ("John Doe", "john.doe@example.com")
    encoding = 'utf-8'
    expected = 'John Doe <john.doe@example.com>'
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_with_invalid_string():
    addr = "Invalid Address"
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, encoding)

def test_sanitize_address_with_invalid_tuple():
    addr = ("Invalid Name", "invalid-email")
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid adddress; only'):
        sanitize_address(addr, encoding)

def test_sanitize_address_with_unicode():
    addr = "Иван Иванов <ivan.ivanov@example.com>"
    encoding = 'utf-8'
    expected = 'Иван Иванов <ivan.ivanov@example.com>'
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_with_non_ascii_local_part():
    addr = ("User", "用户@example.com")
    encoding = 'utf-8'
    expected = 'User <用户@example.com>'
    result = sanitize_address(addr, encoding)
    assert result == expected

def test_sanitize_address_with_non_ascii_domain():
    addr = ("User", "user@例子.测试")
    encoding = 'utf-8'
    expected = 'User <user@例子.测试>'
    result = sanitize_address(addr, encoding)
    assert result == expected