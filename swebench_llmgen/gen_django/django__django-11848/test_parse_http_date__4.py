import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_valid_formats():
    # Testing RFC1123 date format
    result = parse_http_date("Wed, 21 Oct 2015 07:28:00 GMT")
    expected = calendar.timegm(datetime.datetime(2015, 10, 21, 7, 28, 0).utctimetuple())
    assert result == expected

    # Testing RFC850 date format
    result = parse_http_date("Sunday, 06-Nov-94 08:49:37 GMT")
    expected = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert result == expected

    # Testing ASCTIME date format
    result = parse_http_date("Thu Nov 07 10:28:00 2021")
    expected = calendar.timegm(datetime.datetime(2021, 11, 7, 10, 28, 0).utctimetuple())
    assert result == expected

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError) as excinfo:
        parse_http_date("Invalid Date String")
    assert "is not in a valid HTTP date format" in str(excinfo.value)

def test_parse_http_date_year_less_than_70():
    result = parse_http_date("Wed, 10 Oct 69 07:28:00 GMT")
    expected = calendar.timegm(datetime.datetime(2069, 10, 10, 7, 28, 0).utctimetuple())
    assert result == expected

def test_parse_http_date_year_between_70_and_99():
    result = parse_http_date("Wed, 10 Oct 79 07:28:00 GMT")
    expected = calendar.timegm(datetime.datetime(1979, 10, 10, 7, 28, 0).utctimetuple())
    assert result == expected