import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_rfc1123():
    date_str = "Mon, 15 Feb 2021 12:30:45 GMT"
    result = parse_http_date(date_str)
    expected = calendar.timegm(datetime.datetime(2021, 2, 15, 12, 30, 45).utctimetuple())
    assert result == expected

def test_parse_http_date_rfc850():
    date_str = "Sunday, 06-Nov-94 08:49:37 GMT"
    result = parse_http_date(date_str)
    expected = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert result == expected

def test_parse_http_date_asctime():
    date_str = "Sun Nov  6 08:49:37 1994"
    result = parse_http_date(date_str)
    expected = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert result == expected

def test_parse_http_date_invalid():
    with pytest.raises(ValueError):
        parse_http_date("Invalid date string")

def test_parse_http_date_year_less_than_70():
    date_str = "Mon, 15 Feb 69 12:30:45 GMT"
    result = parse_http_date(date_str)
    expected = calendar.timegm(datetime.datetime(1969, 2, 15, 12, 30, 45).utctimetuple())
    assert result == expected

def test_parse_http_date_year_between_70_and_99():
    date_str = "Mon, 15 Feb 84 12:30:45 GMT"
    result = parse_http_date(date_str)
    expected = calendar.timegm(datetime.datetime(1984, 2, 15, 12, 30, 45).utctimetuple())
    assert result == expected