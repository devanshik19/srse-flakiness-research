import pytest
from django.utils.dateformat import DateFormat
import datetime

def test_y_method():
    # Test with a date in the 20th century
    date_1999 = datetime.datetime(year=1999, month=1, day=1)
    formatter_1999 = DateFormat()
    formatter_1999.data = date_1999
    assert formatter_1999.y() == '99'

    # Test with a date in the 21st century
    date_2023 = datetime.datetime(year=2023, month=1, day=1)
    formatter_2023 = DateFormat()
    formatter_2023.data = date_2023
    assert formatter_2023.y() == '23'

    # Test with a year before the century mark
    date_2000 = datetime.datetime(year=2000, month=1, day=1)
    formatter_2000 = DateFormat()
    formatter_2000.data = date_2000
    assert formatter_2000.y() == '00'

    # Test with a year in the 21st century beyond the first two decades
    date_2025 = datetime.datetime(year=2025, month=1, day=1)
    formatter_2025 = DateFormat()
    formatter_2025.data = date_2025
    assert formatter_2025.y() == '25'