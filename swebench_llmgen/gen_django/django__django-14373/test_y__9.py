import pytest
import datetime
from django.utils.dateformat import DateFormat

@pytest.mark.parametrize("year, expected_output", [
    (1999, '99'),
    (2000, '00'),
    (2023, '23'),
    (1900, '00'),
    (2100, '00'),
])
def test_y(year, expected_output):
    date = datetime.datetime(year, 1, 1)
    df = DateFormat()
    df.data = date  # Assigning the date to the data attribute of DateFormat
    assert df.y() == expected_output