import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import AppRegistryNotReady

@pytest.fixture
def apps_instance():
    return apps

def test_clear_cache(apps_instance):
    # Ensure the cache is populated initially
    user_model = apps_instance.get_model('auth', 'User')
    user_instance = User(username='testuser')
    user_instance.save()
    
    # Check that the model cache is populated
    assert user_model.objects.count() == 1
    
    # Now clear the cache
    apps_instance.clear_cache()
    
    # Verify that the model cache has been cleared
    # The cache should still return the model class but the instance should not be available.
    assert user_model.objects.count() == 1
    
    # Create a new user to ensure the cache is working again correctly after clear
    new_user_instance = User(username='newtestuser')
    new_user_instance.save()
    
    # After re-populating the cache, we should see the new user
    assert user_model.objects.count() == 2
    
    # Clear the cache again to verify the intended behavior
    apps_instance.clear_cache()
    assert user_model.objects.count() == 2  # Should still work after clearing, as new cache created again