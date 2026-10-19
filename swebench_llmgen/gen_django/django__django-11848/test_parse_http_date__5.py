import pytest
from django.utils.http import parse_http_date

def test_parse_http_date_rfc1123():
    assert parse_http_date("Tue, 15 Nov 1994 12:45:26 GMT") == 784111526
    assert parse_http_date("Wed, 21 Oct 2015 07:28:00 GMT") == 1445414880

def test_parse_http_date_rfc850():
    assert parse_http_date("Sunday, 06-Nov-94 08:49:37 GMT") == 784111777
    assert parse_http_date("Saturday, 29-Oct-16 18:32:15 GMT") == 1477769535

def test_parse_http_date_asctime():
    assert parse_http_date("Wed Oct  4 00:00:00 2000") == 978307200
    assert parse_http_date("Fri Mar  3 03:03:03 2023") == 1677810183

def test_parse_http_date_invalid_format():
    with pytest.raises(ValueError):
        parse_http_date("Invalid date format")
    
    with pytest.raises(ValueError):
        parse_http_date("Not a real date")
    
    with pytest.raises(ValueError):
        parse_http_date("32 Nov 2020 25:61:00 GMT")