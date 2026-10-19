import pytest
from django.apps import Apps
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_clear_cache():
    # Create an AppConfig to use for testing
    app_config = Apps(installed_apps=['django.contrib.auth'])

    # Get a model and ensure it is fetched and cached
    user_model = app_config.get_model('auth', 'User')
    assert user_model is not None

    # Check that the cache is populated
    assert user_model._meta._get_fields_cache() is not None

    # Clear the cache
    app_config.clear_cache()

    # After clearing the cache, the fields cache should be empty
    assert user_model._meta._get_fields_cache() is None

    # Re-fetch the model to ensure it's still accessible after clearing
    user_model_after_clear = app_config.get_model('auth', 'User')
    assert user_model_after_clear is not None

    # Make sure the cache is re-populated properly
    assert user_model_after_clear._meta._get_fields_cache() is not None