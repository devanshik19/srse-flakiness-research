import pytest
from django.utils.dateformat import DateFormat
import datetime

def test_y_method():
    # Test case for the year 2000
    date_format = DateFormat()
    date_format.data = datetime.datetime(2000, 1, 1)
    assert date_format.y() == '00'

    # Test case for the year 2023
    date_format.data = datetime.datetime(2023, 1, 1)
    assert date_format.y() == '23'

    # Test case for the year 1999
    date_format.data = datetime.datetime(1999, 1, 1)
    assert date_format.y() == '99'

    # Test case for the year 2100
    date_format.data = datetime.datetime(2100, 1, 1)
    assert date_format.y() == '00'  # because of modulo 100

    # Test case for the year 2150
    date_format.data = datetime.datetime(2150, 1, 1)
    assert date_format.y() == '50'