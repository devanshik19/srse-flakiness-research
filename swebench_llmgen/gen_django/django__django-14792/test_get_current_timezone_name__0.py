import pytest
from django.utils import timezone
from django.contrib.auth.models import User

def test_get_current_timezone_name():
    # Set up a user to ensure the Django context can determine the timezone
    user = User.objects.create_user(username='testuser', password='password')
    
    # Test with default time zone
    timezone.activate(pytz.timezone('UTC'))
    assert timezone.get_current_timezone_name() == 'UTC'

    # Test with a different time zone
    timezone.activate(pytz.timezone('America/New_York'))
    assert timezone.get_current_timezone_name() == 'America/New_York'

    # Clean up
    timezone.deactivate()  # Reset to the initial timezone