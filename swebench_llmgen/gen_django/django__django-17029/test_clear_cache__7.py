import pytest
from django.apps.registry import Apps
from django.contrib.auth.models import User

def test_clear_cache():
    # Initialize the Apps instance with a list of installed apps
    apps = Apps(['django.contrib.auth', 'django.contrib.contenttypes'])
    
    # Verify that models are loaded initially
    assert len(apps.get_models(include_auto_created=True)) > 0

    # Get a model from the Apps instance
    UserModel = apps.get_model('auth', 'User')

    # Access the model's _meta to ensure it's available
    assert UserModel._meta is not None

    # Clear the cache
    apps.clear_cache()

    # Now try to access the model's _meta again to ensure cache is expired
    UserModel._meta._expire_cache_called = False  # Adding custom attribute for assertion
    
    def expire_cache_hook(*args, **kwargs):
        UserModel._meta._expire_cache_called = True

    # Hooking expire_cache method to simulate clearing the cache
    original_method = UserModel._meta._expire_cache
    UserModel._meta._expire_cache = expire_cache_hook

    # Call clear_cache, which should call _expire_cache
    apps.clear_cache()

    # Check if _expire_cache has been called
    assert UserModel._meta._expire_cache_called is True

    # Restore original method
    UserModel._meta._expire_cache = original_method