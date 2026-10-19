import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model

# Set up a custom user model in settings for testing
settings.AUTH_USER_MODEL = 'auth.User'

def test_check_user_model_requires_fields_list():
    User.REQUIRED_FIELDS = 'not_a_list'
    errors = check_user_model()
    assert any(error.id == 'auth.E001' for error in errors)

def test_check_user_model_username_in_required_fields():
    User.REQUIRED_FIELDS = [User.USERNAME_FIELD]
    errors = check_user_model()
    assert any(error.id == 'auth.E002' for error in errors)

def test_check_user_model_username_field_unique():
    User._meta.get_field(User.USERNAME_FIELD).unique = False
    errors = check_user_model()
    assert any(error.id == 'auth.E003' for error in errors)

def test_check_user_model_methods_as_properties():
    class CustomUser(User):
        def is_anonymous(self):
            return False
        
        def is_authenticated(self):
            return True
            
    apps.get_model = lambda app_label, model_name: CustomUser
    settings.AUTH_USER_MODEL = 'test.CustomUser'
    errors = check_user_model()
    assert any(error.id == 'auth.C009' for error in errors)
    assert any(error.id == 'auth.C010' for error in errors)

def test_check_user_model_success():
    User.REQUIRED_FIELDS = []
    User._meta.get_field(User.USERNAME_FIELD).unique = True
    errors = check_user_model()
    assert errors == []