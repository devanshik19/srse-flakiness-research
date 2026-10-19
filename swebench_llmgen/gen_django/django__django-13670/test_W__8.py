import datetime
import pytest
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat

@pytest.fixture
def date_format_instance():
    # Create a date object for the test
    date = datetime.datetime(2023, 1, 1)  # This date is in ISO week 52
    df = DateFormat()
    df.data = date  # Set the data attribute to our test date
    return df

def test_week_number(date_format_instance):
    # Test the week number from the date (2023-01-01)
    assert date_format_instance.W() == 52  # January 1, 2023 is in week 52 of 2022