import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_valid_rfc1123():
    date = "Mon, 15 Jan 2021 12:45:30 GMT"
    result = parse_http_date(date)
    expected = int(datetime.datetime(2021, 1, 15, 12, 45, 30).timestamp())
    assert result == expected

def test_parse_http_date_valid_rfc850():
    date = "Sunday, 06-Nov-94 08:49:37 GMT"
    result = parse_http_date(date)
    expected = int(datetime.datetime(1994, 11, 6, 8, 49, 37).timestamp())
    assert result == expected

def test_parse_http_date_valid_asctime():
    date = "Sun Nov  6 08:49:37 1994"
    result = parse_http_date(date)
    expected = int(datetime.datetime(1994, 11, 6, 8, 49, 37).timestamp())
    assert result == expected

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError, match=r"'Invalid date' is not in a valid HTTP date format"):
        parse_http_date("Invalid date")

def test_parse_http_date_invalid_year():
    with pytest.raises(ValueError, match=r"'Year 3000-01-01 00:00:00' is not a valid date"):
        parse_http_date("Sun, 01 Jan 3000 00:00:00 GMT")

def test_parse_http_date_year_less_than_70():
    date = "Mon, 01 Jan 69 00:00:00 GMT"
    result = parse_http_date(date)
    expected = int(datetime.datetime(1969, 1, 1, 0, 0, 0).timestamp())
    assert result == expected

def test_parse_http_date_year_between_70_and_99():
    date = "Mon, 01 Jan 99 00:00:00 GMT"
    result = parse_http_date(date)
    expected = int(datetime.datetime(1999, 1, 1, 0, 0, 0).timestamp())
    assert result == expected