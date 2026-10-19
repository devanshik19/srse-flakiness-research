import pytest
import datetime
from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User

@pytest.fixture
def setup_date_format():
    user = User.objects.create_user(username='testuser', password='testpass')
    date_to_format = datetime.datetime(2023, 5, 1)  # A Monday in the year 2023
    return DateFormat(date_to_format)

def test_week_number_monday(setup_date_format):
    date_format = setup_date_format
    assert date_format.W() == 18  # 1st week of May 2023 is the 18th week of the year

def test_week_number_not_monday():
    date_format = DateFormat(datetime.datetime(2023, 5, 2))  # A Tuesday in the same week
    assert date_format.W() == 18  # Should still return the same week number

def test_week_number_end_of_year():
    date_format = DateFormat(datetime.datetime(2023, 12, 31))  # Last day of the year
    assert date_format.W() == 52  # Last week of 2023

def test_week_number_new_year():
    date_format = DateFormat(datetime.datetime(2024, 1, 1))  # First day of the new year
    assert date_format.W() == 1  # First week of 2024