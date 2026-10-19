import pytest
from django.utils.dateformat import DateFormat
from django.utils import timezone
from datetime import datetime

@pytest.mark.parametrize(
    "year, expected",
    [(1999, '99'), (2000, '00'), (2015, '15'), (2023, '23'), (-1, '01')]
)
def test_y(year, expected):
    dt = datetime(year, 1, 1)  # create a datetime object for January 1st of the year
    date_format = DateFormat()
    date_format.data = dt  # Set the data attribute to the datetime object
    assert date_format.y() == expected