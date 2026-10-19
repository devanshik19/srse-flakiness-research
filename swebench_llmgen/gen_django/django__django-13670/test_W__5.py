import datetime
import pytest
from django.utils.dateformat import DateFormat

@pytest.mark.parametrize("date_input, expected_week_number", [
    (datetime.date(2023, 1, 1), 52),  # Last week of 2022
    (datetime.date(2023, 1, 2), 1),   # First week of 2023
    (datetime.date(2023, 7, 10), 28),  # Week of July 10, 2023
    (datetime.date(2023, 12, 31), 52), # Last week of 2023
])
def test_W(date_input, expected_week_number):
    date_format = DateFormat()
    date_format.data = date_input
    assert date_format.W() == expected_week_number

def test_W_with_aware_datetime():
    date_input = datetime.datetime(2023, 1, 2, tzinfo=datetime.timezone.utc)
    date_format = DateFormat()
    date_format.data = date_input
    assert date_format.W() == 1  # First week of 2023

def test_W_with_naive_datetime():
    date_input = datetime.datetime(2023, 1, 2)  # Naive datetime
    date_format = DateFormat()
    date_format.data = date_input
    assert date_format.W() == 1  # First week of 2023