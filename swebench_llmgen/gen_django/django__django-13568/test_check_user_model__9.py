import pytest
from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core import checks
from django.test import TestCase
from itertools import chain

# Custom User Model for testing
class CustomUser(User):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

@pytest.fixture
def custom_user_model():
    # Registering the custom user model
    apps.get_app_config('auth').models['customuser'] = CustomUser
    return CustomUser

def test_check_user_model_with_default_model():
    settings.AUTH_USER_MODEL = 'auth.User'
    errors = check_user_model()
    assert errors == []

def test_check_user_model_with_custom_model(custom_user_model):
    settings.AUTH_USER_MODEL = 'app_name.CustomUser'  # Adjust the app_name accordingly
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 0

def test_check_required_fields_not_list(custom_user_model):
    # Modify the CustomUser model for this test
    custom_user_model.REQUIRED_FIELDS = "not_a_list"
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'

def test_username_field_in_required_fields(custom_user_model):
    custom_user_model.REQUIRED_FIELDS = ['username']
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'

def test_username_field_not_unique(custom_user_model):
    custom_user_model._meta.get_field = lambda field: types.SimpleNamespace(unique=False)
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'

def test_is_anonymous_method(custom_user_model):
    custom_user_model.is_anonymous = MethodType(lambda self: True, custom_user_model)
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 1
    assert errors[0].id == 'auth.C009'

def test_is_authenticated_method(custom_user_model):
    custom_user_model.is_authenticated = MethodType(lambda self: True, custom_user_model)
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 1
    assert errors[0].id == 'auth.C010'