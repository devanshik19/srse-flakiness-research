import pytest
from django.utils.timezone import get_current_timezone_name
from django.utils import timezone

def test_get_current_timezone_name():
    # Set a specific timezone
    timezone.activate(pytz.timezone('America/New_York'))
    assert get_current_timezone_name() == 'America/New_York'

    # Set another timezone
    timezone.activate(pytz.timezone('Europe/London'))
    assert get_current_timezone_name() == 'Europe/London'

    # Deactivate timezone and check default
    timezone.deactivate()
    assert get_current_timezone_name() == 'UTC' # Assuming 'UTC' is the default timezone when no timezone is active