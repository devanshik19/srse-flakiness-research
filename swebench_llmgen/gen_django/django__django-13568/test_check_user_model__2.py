import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model

def test_check_user_model_no_app_configs():
    # Valid user model with REQUIRED_FIELDS as a list
    user_model = get_user_model()
    user_model.REQUIRED_FIELDS = ['email']
    user_model.USERNAME_FIELD = 'username'
    errors = check_user_model()
    
    assert errors == []
    
    # REQUIRED_FIELDS as a non-list/tuple
    user_model.REQUIRED_FIELDS = 'email'
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'

    # USERNAME_FIELD in REQUIRED_FIELDS
    user_model.REQUIRED_FIELDS = ['username', 'email']
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'

    # USERNAME_FIELD not unique
    user_model.REQUIRED_FIELDS = ['email']
    user_model._meta.get_field(user_model.USERNAME_FIELD).unique = False
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'

    # USERNAME_FIELD not unique with a different backend
    settings.AUTHENTICATION_BACKENDS = ['custom.backend']
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.W004'

    # Check for is_anonymous method
    user_model.is_anonymous = lambda self: True
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.C009'

    # Check for is_authenticated method
    user_model.is_authenticated = lambda self: True
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].id == 'auth.C010'

def test_check_user_model_with_app_configs():
    # Create a custom user model with specific app_config
    from django.contrib.auth import get_user_model
    from django.apps import AppConfig

    class CustomUserConfig(AppConfig):
        name = 'custom_user'
        label = 'custom_user'

    custom_user_model = get_user_model()
    custom_user_model._meta.label = CustomUserConfig.label
    custom_user_model.REQUIRED_FIELDS = ['email']
    custom_user_model.USERNAME_FIELD = 'username'

    app_configs = [CustomUserConfig()]

    # Run check with app_config
    errors = check_user_model(app_configs=app_configs)
    assert errors == []

    # Test with USERNAME_FIELD in REQUIRED_FIELDS
    custom_user_model.REQUIRED_FIELDS = ['username']
    errors = check_user_model(app_configs=app_configs)
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'