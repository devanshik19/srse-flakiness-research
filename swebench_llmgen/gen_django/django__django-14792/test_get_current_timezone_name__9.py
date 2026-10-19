import pytest
import pytz
from django.utils.timezone import get_current_timezone_name
from django.contrib.auth.models import User

@pytest.mark.parametrize("timezone_str, expected", [
    ("UTC", "UTC"),
    ("America/New_York", "America/New_York"),
    ("Europe/London", "Europe/London"),
])
def test_get_current_timezone_name(timezone_str, expected):
    user = User.objects.create_user(username='testuser', password='password')
    with pytz.timezone(timezone_str).localize(datetime.now()) as tz:
        if timezone_str == "UTC":
            settings.TIME_ZONE = 'UTC'  # Set the timezone in settings
        else:
            settings.TIME_ZONE = timezone_str
        
        assert get_current_timezone_name() == expected