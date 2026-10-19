import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_rfc1123():
    date_str = "Wed, 21 Oct 2015 07:28:00 GMT"
    expected = calendar.timegm(datetime.datetime(2015, 10, 21, 7, 28, 0).utctimetuple())
    assert parse_http_date(date_str) == expected

def test_parse_http_date_rfc850():
    date_str = "Sunday, 06-Nov-94 08:49:37 GMT"
    expected = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert parse_http_date(date_str) == expected

def test_parse_http_date_asctime():
    date_str = "Sat Nov  6 08:49:37 1994"
    expected = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert parse_http_date(date_str) == expected

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError) as excinfo:
        parse_http_date("Invalid date format")
    assert "Invalid date format" in str(excinfo.value)

def test_parse_http_date_year_less_than_70():
    date_str = "Fri, 01 Jan 69 00:00:00 GMT"
    expected = calendar.timegm(datetime.datetime(2069, 1, 1, 0, 0, 0).utctimetuple())
    assert parse_http_date(date_str) == expected

def test_parse_http_date_year_between_70_and_99():
    date_str = "Fri, 01 Jan 79 00:00:00 GMT"
    expected = calendar.timegm(datetime.datetime(1979, 1, 1, 0, 0, 0).utctimetuple())
    assert parse_http_date(date_str) == expected