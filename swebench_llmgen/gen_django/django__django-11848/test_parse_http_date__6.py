import pytest
import datetime
from django.utils.http import parse_http_date

# Define the date formats according to RFC1123, RFC850, and ASCTIME
RFC1123_DATE = re.compile(r'(?P<mon>[A-Za-z]{3}), (?P<day>\d{2}) (?P<mon>[A-Za-z]{3}) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) GMT')
RFC850_DATE = re.compile(r'(?P<mon>[A-Za-z]{3}, \d{2} \d{6} GMT)')
ASCTIME_DATE = re.compile(r'(?P<mon>[A-Za-z]{3}  *\d{1,2} \d{2}:\d{2}:\d{2} \d{4})')

MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun", 
    "jul", "aug", "sep", "oct", "nov", "dec"
]

def test_parse_http_date_valid_rfc1123():
    assert parse_http_date("Mon, 20 Jun 2022 15:35:22 GMT") == 1655739322

def test_parse_http_date_valid_rfc850():
    assert parse_http_date("Sunday, 20-Jun-22 15:35:22 GMT") == 1655739322

def test_parse_http_date_valid_asctime():
    assert parse_http_date("Sun Jun 20 15:35:22 2022") == 1655739322

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError, match="is not in a valid HTTP date format"):
        parse_http_date("Invalid date format")

def test_parse_http_date_invalid_day():
    with pytest.raises(ValueError, match="is not a valid date"):
        parse_http_date("Mon, 32 Jun 2022 15:35:22 GMT")

def test_parse_http_date_invalid_month():
    with pytest.raises(ValueError, match="is not a valid date"):
        parse_http_date("Mon, 20 Junv 2022 15:35:22 GMT")

def test_parse_http_date_invalid_year():
    with pytest.raises(ValueError, match="is not a valid date"):
        parse_http_date("Mon, 20 2022 15:35:22 GMT")