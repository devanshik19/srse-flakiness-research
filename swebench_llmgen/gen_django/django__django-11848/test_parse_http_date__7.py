import pytest
import datetime
from django.utils.http import parse_http_date

# Constants used for parsing
RFC1123_DATE = re.compile(r'(?P<day>\d{2}) (?P<mon>\w{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) GMT')
RFC850_DATE = re.compile(r'(?P<mon>\w{3}), (?P<day>\d{2}) (?P<year>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})')
ASCTIME_DATE = re.compile(r'(?P<mon>\w{3}) (?P<day>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) (?P<year>\d{4})')

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

def test_parse_http_date_rfc1123():
    date_str = "Mon, 15 Aug 2022 15:30:45 GMT"
    expected_epoch = calendar.timegm(datetime.datetime(2022, 8, 15, 15, 30, 45).utctimetuple())
    assert parse_http_date(date_str) == expected_epoch

def test_parse_http_date_rfc850():
    date_str = "Sunday, 06-Nov-94 08:49:37 GMT"
    expected_epoch = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert parse_http_date(date_str) == expected_epoch

def test_parse_http_date_asctime():
    date_str = "Sun Nov  6 08:49:37 1994"
    expected_epoch = calendar.timegm(datetime.datetime(1994, 11, 6, 8, 49, 37).utctimetuple())
    assert parse_http_date(date_str) == expected_epoch

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError):
        parse_http_date("Invalid date format")

def test_parse_http_date_year_less_than_100():
    date_str = "Mon, 15 Aug 69 15:30:45 GMT"
    expected_epoch = calendar.timegm(datetime.datetime(2069, 8, 15, 15, 30, 45).utctimetuple())
    assert parse_http_date(date_str) == expected_epoch

def test_parse_http_date_year_ambiguous():
    date_str = "Mon, 15 Aug 99 15:30:45 GMT"
    expected_epoch = calendar.timegm(datetime.datetime(1999, 8, 15, 15, 30, 45).utctimetuple())
    assert parse_http_date(date_str) == expected_epoch