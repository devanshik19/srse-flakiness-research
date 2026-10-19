import pytest
import pytz
from django.utils.timezone import get_current_timezone_name
from django.conf import settings

def test_get_current_timezone_name_setting_pacific():
    settings.TIME_ZONE = 'America/Los_Angeles'
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    assert get_current_timezone_name() == 'America/Los_Angeles'
    
def test_get_current_timezone_name_setting_utc():
    settings.TIME_ZONE = 'UTC'
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    assert get_current_timezone_name() == 'UTC'

def test_get_current_timezone_name_setting_eastern():
    settings.TIME_ZONE = 'America/New_York'
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    assert get_current_timezone_name() == 'America/New_York'

def test_get_current_timezone_name_setting_central():
    settings.TIME_ZONE = 'America/Chicago'
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    assert get_current_timezone_name() == 'America/Chicago'