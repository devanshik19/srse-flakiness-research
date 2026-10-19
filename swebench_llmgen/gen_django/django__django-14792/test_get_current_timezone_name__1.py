import pytest
from django.utils.timezone import get_current_timezone_name
from django.utils import timezone

def test_get_current_timezone_name():
    # Set the default timezone to 'UTC'
    timezone.activate(pytz.UTC)
    assert get_current_timezone_name() == 'UTC'
    
    # Set the default timezone to 'America/New_York'
    timezone.activate(pytz.timezone('America/New_York'))
    assert get_current_timezone_name() == 'America/New_York'
    
    # Reset to system default timezone (may vary based on system settings)
    timezone.deactivate()
    assert get_current_timezone_name() != 'America/New_York'