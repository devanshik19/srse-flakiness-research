import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.apps import apps
from django.conf import settings

def test_check_user_model_with_default_user_model():
    # Check that the default User model is valid
    errors = check_user_model()
    assert errors == []

def test_check_user_model_with_custom_user_model():
    # Create a custom user model with specific requirements
    from django.db import models

    class CustomUser(models.Model):
        username = models.CharField(max_length=150, unique=True)
        email = models.EmailField()
        REQUIRED_FIELDS = ['email']
        USERNAME_FIELD = 'username'

        @property
        def is_anonymous(self):
            return False

        @property
        def is_authenticated(self):
            return True

    # Register the custom model
    apps.register_model('auth', CustomUser)
    settings.AUTH_USER_MODEL = 'auth.CustomUser'

    # Perform the check
    errors = check_user_model(apps.get_app_config('auth').get_models())

    # Validate the errors
    assert len(errors) == 0

    # Test REQUIRED_FIELDS validation
    CustomUser.REQUIRED_FIELDS = 'email'  # Make REQUIRED_FIELDS not a list/tuple
    errors = check_user_model(apps.get_app_config('auth').get_models())
    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'

    # Test USERNAME_FIELD inclusion in REQUIRED_FIELDS
    CustomUser.REQUIRED_FIELDS = ['username', 'email']
    errors = check_user_model(apps.get_app_config('auth').get_models())
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'

    # Test uniqueness of USERNAME_FIELD
    CustomUser._meta.get_field('username').unique = False
    errors = check_user_model(apps.get_app_config('auth').get_models())
    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'

    # Test is_anonymous method issue
    CustomUser.is_anonymous = lambda self: True  # Incorrectly set as method
    errors = check_user_model(apps.get_app_config('auth').get_models())
    assert len(errors) == 1
    assert errors[0].id == 'auth.C009'
  
    # Test is_authenticated method issue
    CustomUser.is_authenticated = lambda self: True  # Incorrectly set as method
    errors = check_user_model(apps.get_app_config('auth').get_models())
    assert len(errors) == 1
    assert errors[0].id == 'auth.C010'