import pytest
from django.utils.dateformat import DateFormat
import datetime

def test_y_should_return_year_with_leading_zeros():
    # Test case 1: Year 1999
    date_format_1999 = DateFormat()
    date_format_1999.data = datetime.datetime(1999, 1, 1)
    assert date_format_1999.y() == '99'

    # Test case 2: Year 2000
    date_format_2000 = DateFormat()
    date_format_2000.data = datetime.datetime(2000, 1, 1)
    assert date_format_2000.y() == '00'

    # Test case 3: Year 2015
    date_format_2015 = DateFormat()
    date_format_2015.data = datetime.datetime(2015, 1, 1)
    assert date_format_2015.y() == '15'

    # Test case 4: Year 2021
    date_format_2021 = DateFormat()
    date_format_2021.data = datetime.datetime(2021, 1, 1)
    assert date_format_2021.y() == '21'

    # Test case 5: Year 2099
    date_format_2099 = DateFormat()
    date_format_2099.data = datetime.datetime(2099, 1, 1)
    assert date_format_2099.y() == '99'