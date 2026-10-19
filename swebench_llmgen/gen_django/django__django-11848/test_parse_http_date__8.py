import pytest
import datetime
from django.utils.http import parse_http_date

def test_parse_http_date_rfc1123():
    assert parse_http_date("Mon, 25 Oct 2021 14:48:00 GMT") == int(datetime.datetime(2021, 10, 25, 14, 48, 0, tzinfo=datetime.timezone.utc).timestamp())
    
def test_parse_http_date_rfc850():
    assert parse_http_date("Sunday, 26-Oct-21 14:48:00 GMT") == int(datetime.datetime(2021, 10, 26, 14, 48, 0, tzinfo=datetime.timezone.utc).timestamp())
    
def test_parse_http_date_asctime():
    assert parse_http_date("Sun Oct 26 14:48:00 2021") == int(datetime.datetime(2021, 10, 26, 14, 48, 0, tzinfo=datetime.timezone.utc).timestamp())

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError, match=r"\"invalid_date\" is not in a valid HTTP date format"):
        parse_http_date("invalid_date")

def test_parse_http_date_invalid_date():
    with pytest.raises(ValueError, match=r"\"Mon, 25 Oct 2100 25:61:00 GMT\" is not a valid date"):
        parse_http_date("Mon, 25 Oct 2100 25:61:00 GMT")

def test_parse_http_date_year_edge_case():
    assert parse_http_date("Mon, 01 Jan 69 00:00:00 GMT") == int(datetime.datetime(1969, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp())
    assert parse_http_date("Mon, 01 Jan 70 00:00:00 GMT") == int(datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp())