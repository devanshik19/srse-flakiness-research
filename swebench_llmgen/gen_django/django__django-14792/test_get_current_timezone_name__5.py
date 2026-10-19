import pytest
from django.utils.timezone import get_current_timezone_name
from django.contrib.auth.models import User
import pytz

def test_get_current_timezone_name_utc():
    # Set the timezone to UTC
    pytz.timezone('UTC')
    current_timezone_name = get_current_timezone_name()
    assert current_timezone_name == 'UTC', f'Expected "UTC" but got {current_timezone_name}'

def test_get_current_timezone_name_local():
    # Set the timezone to a local timezone, e.g., 'America/New_York'
    pytz.timezone('America/New_York')
    current_timezone_name = get_current_timezone_name()
    assert current_timezone_name == 'America/New_York', f'Expected "America/New_York" but got {current_timezone_name}'

def test_get_current_timezone_name_asia_tokyo():
    # Set the timezone to 'Asia/Tokyo'
    pytz.timezone('Asia/Tokyo')
    current_timezone_name = get_current_timezone_name()
    assert current_timezone_name == 'Asia/Tokyo', f'Expected "Asia/Tokyo" but got {current_timezone_name}'

def test_get_current_timezone_name_invalid():
    # Test for when an invalid timezone might be set. 
    # Assuming this is handled and defaults to UTC.
    with pytest.raises(pytz.UnknownTimeZoneError):
        pytz.timezone('Invalid/Timezone')
    current_timezone_name = get_current_timezone_name()
    assert current_timezone_name is not None, 'Expected a timezone name but got None'