import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_valid_rfc1123():
    # Valid RFC1123 date
    assert parse_http_date('Mon, 21 Oct 2019 07:28:00 GMT') == 1571641680

def test_parse_http_date_valid_rfc850():
    # Valid RFC850 date
    assert parse_http_date('Monday, 21-Oct-19 07:28:00 GMT') == 1571641680

def test_parse_http_date_valid_asctime():
    # Valid asctime date
    assert parse_http_date('Mon Oct 21 07:28:00 2019') == 1571641680

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError) as excinfo:
        parse_http_date('Invalid Date Format')
    assert str(excinfo.value) == "'Invalid Date Format' is not in a valid HTTP date format"

def test_parse_http_date_invalid_year():
    with pytest.raises(ValueError) as excinfo:
        parse_http_date('Mon, 21 Oct 1969 07:28:00 GMT')  # This should still work
    assert str(excinfo.value) == "'Mon, 21 Oct 1969 07:28:00 GMT' is not a valid date"  # Invalid year handling

def test_parse_http_date_year_conversion():
    # Test year conversion
    assert parse_http_date('Mon, 21 Oct 69 07:28:00 GMT') == 2069221680  # 2069 after conversion