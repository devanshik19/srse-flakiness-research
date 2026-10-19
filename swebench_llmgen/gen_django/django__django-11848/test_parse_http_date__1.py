import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_valid_rfc1123():
    assert parse_http_date("Mon, 01 Jan 2000 00:00:00 GMT") == 946684800

def test_parse_http_date_valid_rfc850():
    assert parse_http_date("Sunday, 06-Nov-94 08:49:37 GMT") == 785611777

def test_parse_http_date_valid_asctime():
    assert parse_http_date("Sun Nov  6 08:49:37 1994") == 785611777

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError, match=r"'not-a-date' is not in a valid HTTP date format"):
        parse_http_date("not-a-date")

def test_parse_http_date_year_too_low():
    with pytest.raises(ValueError, match=r"'00 Jan 01 00:00:00 GMT' is not a valid date"):
        parse_http_date("00 Jan 01 00:00:00 GMT")

def test_parse_http_date_year_too_high():
    assert parse_http_date("Mon, 01 Jan 2075 00:00:00 GMT") == 1775692800

def test_parse_http_date_feb_29_leap_year():
    assert parse_http_date("Fri, 29 Feb 2008 00:00:00 GMT") == 1204224000

def test_parse_http_date_feb_29_non_leap_year():
    with pytest.raises(ValueError, match=r"'Sat, 29 Feb 2019 00:00:00 GMT' is not a valid date"):
        parse_http_date("Sat, 29 Feb 2019 00:00:00 GMT")