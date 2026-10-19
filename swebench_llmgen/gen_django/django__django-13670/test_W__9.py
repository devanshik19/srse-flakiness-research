import pytest
import datetime
from django.utils.dateformat import DateFormat

def test_W_with_monday_start():
    # Arrange
    date_time = datetime.datetime(2023, 10, 23)  # This is a Monday
    date_format = DateFormat()
    date_format.data = date_time

    # Act
    week_number = date_format.W()

    # Assert
    assert week_number == 43  # The week containing October 23, 2023 is the 43rd week

def test_W_with_sunday_start():
    # Arrange
    date_time = datetime.datetime(2023, 10, 22)  # This is a Sunday
    date_format = DateFormat()
    date_format.data = date_time

    # Act
    week_number = date_format.W()

    # Assert
    assert week_number == 42  # The week containing October 22, 2023 is still the 42nd week

def test_W_with_new_year():
    # Arrange
    date_time = datetime.datetime(2023, 1, 1)  # This is the first day of the year
    date_format = DateFormat()
    date_format.data = date_time

    # Act
    week_number = date_format.W()

    # Assert
    assert week_number == 52  # January 1, 2023 falls in week 52 of the previous year

def test_W_with_leap_year():
    # Arrange
    date_time = datetime.datetime(2020, 2, 29)  # This is a leap day
    date_format = DateFormat()
    date_format.data = date_time

    # Act
    week_number = date_format.W()

    # Assert
    assert week_number == 9  # February 29, 2020 is in the 9th week of the year