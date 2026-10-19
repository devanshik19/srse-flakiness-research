import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import AppRegistryNotReady

@pytest.fixture
def clear_cache_setup():
    # Setup: Register a new user model to ensure the app registry is populated.
    user_config = apps.get_app_config('auth')
    user_model = User
    user_config.register_model(User._meta.label, user_model)
    return user_config

def test_clear_cache(clear_cache_setup):
    app_config = clear_cache_setup
    
    # Ensure the cache is initially populated
    models_before_clear = list(app_config.get_models())
    assert any(model is User for model in models_before_clear)

    # Clear the cache
    apps.clear_cache()
    
    # Ensure the cache has been cleared
    models_after_clear = list(app_config.get_models())
    assert models_after_clear != models_before_clear  # models should differ

    # Call clear_cache again to check it doesn't throw errors on empty cache
    apps.clear_cache()
    
    # Ensure the model still exists after multiple calls
    models_after_multiple_clear = list(app_config.get_models())
    assert models_after_multiple_clear == models_before_clear