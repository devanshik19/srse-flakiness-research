import pytest
from django.utils.timezone import get_current_timezone_name
import pytz
from django.conf import settings

def test_get_current_timezone_name(settings):
    # Test with default timezone settings
    settings.TIME_ZONE = 'UTC'
    assert get_current_timezone_name() == 'UTC'
    
    # Test with a different timezone
    settings.TIME_ZONE = 'America/New_York'
    assert get_current_timezone_name() == 'America/New_York'
    
    # Test with a timezone that may have DST changes
    settings.TIME_ZONE = 'Europe/London'
    assert get_current_timezone_name() == 'Europe/London'
    
    # Test with an invalid timezone, should raise exception
    settings.TIME_ZONE = 'Invalid/Timezone'
    with pytest.raises(pytz.UnknownTimeZoneError):
        get_current_timezone_name()