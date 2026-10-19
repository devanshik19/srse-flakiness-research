import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat

@pytest.mark.parametrize("year, expected", [
    (1999, '99'),
    (2000, '00'),
    (2023, '23'),
    (1987, '87'),
    (1950, '50'),
])
def test_y(year, expected):
    user = User(username='testuser', password='password')
    user.save()

    # Set the date to the specified year
    date = timezone.datetime(year, 1, 1)
    date_format = DateFormat()
    date_format.data = date  # Directly assign the datetime object
    
    assert date_format.y() == expected