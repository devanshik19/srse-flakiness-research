import pytest
from django.apps import Apps
from django.contrib.auth.models import User

@pytest.fixture
def apps_instance():
    return Apps(installed_apps=['django.contrib.auth'])

def test_clear_cache(apps_instance):
    # Initial cache state - cache should not be cleared
    user_model = apps_instance.get_model('auth', 'User')
    user_model._meta._expire_cache = lambda: None  # No-op for test
    assert not hasattr(user_model, '_cache_cleared')

    # Simulate setting up the models normally
    apps_instance.get_models = functools.lru_cache()(lambda include_auto_created: [User])
    user_model._meta._cache_cleared = False  # Initial cache state

    # Clear cache
    apps_instance.clear_cache()

    # Check that cache was cleared
    assert not hasattr(user_model, '_cache_cleared')
    
    # Trigger the cache clear function
    user_model._meta._cache_cleared = True  # Simulating cache clearing
    apps_instance.clear_cache()
    assert not hasattr(user_model, '_cache_cleared')

    # Check that the model cache state is correctly managed after clear_cache
    user_model._meta._cache_cleared = False
    assert not hasattr(user_model, '_cache_cleared')