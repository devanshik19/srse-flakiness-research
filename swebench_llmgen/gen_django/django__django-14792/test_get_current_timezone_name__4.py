import pytest
from django.utils.timezone import get_current_timezone_name
from django.conf import settings
from django.contrib.auth.models import User

def test_get_current_timezone_name():
    # Set the time zone in the settings to test
    settings.TIME_ZONE = 'UTC'
    
    # Create a user to interact with the ORM (not strictly necessary for this test)
    user = User.objects.create_user(username='testuser', password='testpass')
    
    # Get the current timezone name
    timezone_name = get_current_timezone_name()
    
    # Check if the timezone name is what we expect
    assert timezone_name == 'UTC'
    
    # Change the settings to a different timezone
    settings.TIME_ZONE = 'America/New_York'
    
    # Get the updated timezone name
    timezone_name = get_current_timezone_name()
    
    # Check the updated timezone name
    assert timezone_name == 'America/New_York'
    
    # Cleanup
    user.delete()