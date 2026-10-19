import pytest
from datetime import datetime
from django.utils.dateformat import DateFormat

def test_y():
    # Test with a date that results in year '99'
    df = DateFormat()
    df.data = datetime(1999, 1, 1)
    assert df.y() == '99'

    # Test with a date that results in year '00'
    df.data = datetime(2000, 1, 1)
    assert df.y() == '00'

    # Test with a date that results in year '10'
    df.data = datetime(2010, 1, 1)
    assert df.y() == '10'

    # Test with a date that results in year '22'
    df.data = datetime(2022, 1, 1)
    assert df.y() == '22'