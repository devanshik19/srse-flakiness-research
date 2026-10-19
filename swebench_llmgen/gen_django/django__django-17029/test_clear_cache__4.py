import pytest
from django.contrib.auth.models import User
from django.apps import apps

@pytest.fixture
def apps_instance():
    return apps

def test_clear_cache(apps_instance):
    # Ensure models are cached initially
    User.objects.all()  # Access User model to cache it

    # Checking if the cache is present before clearing
    assert User in apps_instance.get_models()
    
    # Call clear_cache and ensure it works as intended
    apps_instance.clear_cache()

    # Now User should no longer be in the cache
    assert User not in apps_instance.get_models()
    
    # Re-access the User model to check the behavior after clear_cache
    User.objects.all()  # Access User model again to refill the cache

    # Validate that the cache is refilled
    assert User in apps_instance.get_models()