import pytest
from django.core.mail.message import sanitize_address
from email.errors import HeaderParseError


def test_sanitize_address_valid_string():
    addr = 'John Doe <john.doe@example.com>'
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    assert result == 'John Doe <john.doe@example.com>'


def test_sanitize_address_valid_tuple():
    addr = ('John Doe', 'john.doe@example.com')
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    assert result == 'John Doe <john.doe@example.com>'


def test_sanitize_address_invalid_string_no_at_symbol():
    addr = 'John Doe john.doe@example.com'
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid address'):
        sanitize_address(addr, encoding)


def test_sanitize_address_invalid_string_invalid_format():
    addr = 'Invalid <John Doe>'
    encoding = 'utf-8'
    with pytest.raises(ValueError, match='Invalid address "Invalid <John Doe>"'):
        sanitize_address(addr, encoding)


def test_sanitize_address_invalid_tuple():
    addr = ('John Doe', 'invalid_email')
    encoding = 'utf-8'
    with pytest.raises(ValueError):
        sanitize_address(addr, encoding)


def test_sanitize_address_non_ascii():
    addr = 'Jöhn Dœ <jöhn.dœ@example.com>'
    encoding = 'utf-8'
    result = sanitize_address(addr, encoding)
    assert result == 'Jöhn Dœ <jöhn.dœ@example.com>'