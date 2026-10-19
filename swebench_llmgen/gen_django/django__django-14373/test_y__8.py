import pytest
from django.utils.dateformat import DateFormat
import datetime

def test_y():
    # Test for a year less than 100
    date_1 = datetime.datetime(2022, 1, 1)
    df_1 = DateFormat()
    df_1.data = date_1
    assert df_1.y() == '22'
    
    # Test for a year above 100
    date_2 = datetime.datetime(1999, 1, 1)
    df_2 = DateFormat()
    df_2.data = date_2
    assert df_2.y() == '99'
    
    # Test for a year that is a century
    date_3 = datetime.datetime(2000, 1, 1)
    df_3 = DateFormat()
    df_3.data = date_3
    assert df_3.y() == '00'
    
    # Test for a year that is before 2000
    date_4 = datetime.datetime(1985, 1, 1)
    df_4 = DateFormat()
    df_4.data = date_4
    assert df_4.y() == '85'