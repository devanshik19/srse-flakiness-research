import pytest
from django.utils.timezone import get_current_timezone_name
from django.utils import timezone

def test_get_current_timezone_name():
    # Set the timezone to a known value
    timezone.activate(pytz.timezone('UTC'))
    assert get_current_timezone_name() == 'UTC'

    timezone.activate(pytz.timezone('America/New_York'))
    assert get_current_timezone_name() == 'America/New_York'

    timezone.deactivate()
    assert get_current_timezone_name() == 'UTC'  # Default timezone after deactivate