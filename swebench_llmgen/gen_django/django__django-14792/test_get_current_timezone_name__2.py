import pytest
from django.utils.timezone import get_current_timezone_name
from django.utils import timezone

def test_get_current_timezone_name():
    # Set active timezone to a known value
    time_zone_name = 'UTC'
    timezone.activate(pytz.timezone(time_zone_name))
    
    # Check if the returned timezone name is as expected
    assert get_current_timezone_name() == time_zone_name

    # Set active timezone to another known value
    time_zone_name = 'America/New_York'
    timezone.activate(pytz.timezone(time_zone_name))
    
    # Check if the returned timezone name is as expected
    assert get_current_timezone_name() == time_zone_name

    # Deactivate timezone to ensure it returns None for the default case
    timezone.deactivate()
    assert get_current_timezone_name() is None