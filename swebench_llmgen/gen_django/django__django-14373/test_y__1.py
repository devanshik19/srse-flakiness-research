import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class DateFormat:
    def __init__(self, data):
        self.data = data

    def y(self):
        """Year, 2 digits with leading zeros; e.g. '99'."""
        return '%02d' % (self.data.year % 100)

def test_date_format_y():
    # Test with a date in the 21st century
    date1 = datetime(2023, 1, 1)
    df1 = DateFormat(date1)
    assert df1.y() == '23'

    # Test with a date in the 20th century
    date2 = datetime(1999, 12, 31)
    df2 = DateFormat(date2)
    assert df2.y() == '99'

    # Test with a date in the year 2000
    date3 = datetime(2000, 1, 1)
    df3 = DateFormat(date3)
    assert df3.y() == '00'
    
    # Test with a date in the year 2100
    date4 = datetime(2100, 1, 1)
    df4 = DateFormat(date4)
    assert df4.y() == '00'